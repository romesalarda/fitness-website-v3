from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Category, Superset, Workout, Exercise

from core.utils import set_m2m_using_ids
from api.utils import check_duplicates

class CategorySerializer(serializers.ModelSerializer):
    '''Serializer for categories'''
    class Meta:
        model = Category
        fields = ("id","title","description")


class ExerciseListSerializer(serializers.ListSerializer):
    '''
    Serializer to handle custom bulk exercise update
    '''
    def update(self, queryset, validated_data):
        exercise_mapping = {exercise.id: exercise for exercise in queryset}
        data_mapping = {item['id']: item for item in validated_data}
        
        result = []
        for exercise_id, data in data_mapping.items():
            exercise = exercise_mapping.get(exercise_id, None)
            if exercise is not None:
                result.append(self.child.update(exercise, data))
        return result


class ExerciseSerializer(serializers.ModelSerializer):
    '''serializer for exercises'''

    id = serializers.UUIDField(required=False)
    user = serializers.ReadOnlyField(source="user.id")
    categories = CategorySerializer(many=True, read_only=True)
    # data on creation
    category_ids = serializers.ListField(write_only=True, required=False)

    class Meta:
        model = Exercise
        fields = (
            "id","title","sets","repetitions","duration","public",
            "categories","user","level","target","direction","rest_period",
            "copy_only","weight","category_ids","weight_unit","cardio_unit",
            "repetitions_unit","resistance_view","distance","description","created"
        )
        list_serializer_class = ExerciseListSerializer

    def create(self, validated_data):
        workout = validated_data.pop("workout", None)
        user = validated_data.pop("user", None)
        title = validated_data.get("title")
        category_ids = validated_data.pop("category_ids", [])

        check_duplicates(workout, "exercises", title=title, 
        err_msg="exercise with the title '%s' already exists in workout" % title)
        
        exercise = self.Meta.model.objects.create(user=user, **validated_data)

        set_m2m_using_ids(Category,
            category_ids, 
            exercise.categories.set,
            error_msg="invalid category ids"
        )
        exercise.save()
        return exercise

    def update(self, instance, validated_data):
        category_ids = validated_data.pop("category_ids", [])
        workout = validated_data.pop("workout", None)
        title = validated_data.get("title")

        set_m2m_using_ids(Category,
            category_ids, 
            instance.categories.set,
            error_msg="invalid category ids"
        )
        # check_duplicates(workout, "exercises", title=title, 
        # err_msg="exercise with the title '%s' already exists in workout" % title)

        return super().update(instance, validated_data)

class SupersetSerializer(serializers.ModelSerializer):
    '''Serializer for workout supersets'''
    id = serializers.UUIDField(required=False)
    exercises = ExerciseSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Superset
        fields = ("id","title","exercises","public","categories","copy_only")

    def create(self, validated_data):
        # extra fields on save can take in the user and workout for validation and saving
        workout = validated_data.pop("workout", None)
        user = validated_data.pop("user", None)
        title = validated_data.get("title")

        check_duplicates(workout, "supersets", title=title, 
        err_msg="superset with the title '%s' already exists in workout" % title)
        
        superset = self.Meta.model.objects.create(user=user,workout=workout, **validated_data)
        return superset

class WorkoutSerializer(serializers.ModelSerializer):
    '''
    Serializer for workout. Updating using this serializer will cascade updates through
    the exercises and supersets
    '''
    user = serializers.ReadOnlyField(source="user.email")
    created = serializers.ReadOnlyField(source="workout.created")
    exercises = ExerciseSerializer(many=True, required=False)
    supersets = SupersetSerializer(many=True, required=False)

    class Meta:
        model = Workout
        fields = ("id","title","user","exercises","created","description","supersets")

    def create(self, validated_data):
        user = validated_data.pop("user", None)
        user_workouts = validated_data.pop("user_workouts", None)
        title = validated_data.get("title")

        check_duplicates(user_workouts, title=title,
        err_msg="Workout with the title '%s' already exists in your library" % title)
        
        workout = self.Meta.model(user=user, **validated_data)
        workout.save()
        return workout

    def update(self, instance, validated_data):
        partial = validated_data.pop("partial", False)
        exercises = validated_data.pop("exercises", [])
        supersets = validated_data.pop("supersets", [])
        # iterate through exercises to update
        for exercise_data in exercises:
            exercise_data = dict(**exercise_data)
            exercise = get_object_or_404(Exercise, id=exercise_data.get("id"))
            # save the instance using the exercise serializer
            serialized = ExerciseSerializer(exercise, data=exercise_data, partial=partial)
            if serialized.is_valid(raise_exception=True):
                serialized.save(workout=instance)
        # iterate through supersets
        for superset in supersets:
            superset_data = dict(**superset)
            superset = get_object_or_404(Superset, id=superset_data.get("id"))
            # save the instance using the exercise serializer
            serialized = SupersetSerializer(superset, data=superset_data, partial=partial)
            if serialized.is_valid(raise_exception=True):
                serialized.save()
        instance.title = validated_data.get("title",instance.title)
        return super().update(instance, validated_data)

class UUIDSerializer(serializers.Serializer):
    '''Serializer used to validate UUID'''
    uuid = serializers.UUIDField()

class TruncatedWorkoutSerializer(serializers.ModelSerializer):
    '''
    Truncated version of user workouts without the supersets
    or exercises.

    Used when we only need to get a list of the 
    workouts if getting all the data is unnecessary.
    '''
    user = serializers.ReadOnlyField(source="user.email")
    created = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()

    class Meta:
        model = Workout
        fields = ("id","title","user","slug","created","last_updated","description")