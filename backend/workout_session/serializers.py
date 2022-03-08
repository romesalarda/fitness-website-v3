from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import WorkoutSession, SessionExercise, SessionSuperset
from builder.models import Workout
from api.utils import check_duplicates

class IndividualExerciseSerializer(serializers.Serializer):
    '''
    Serializer used for validating if an individual exercise is valid
    '''
    rep = serializers.IntegerField(required=False)
    dur = serializers.FloatField(required=False)
    cmplt = serializers.BooleanField(required=False)
    wgt = serializers.FloatField(required=False)

    def create(self, validated_data):
        rep = validated_data.get("rep")
        dur = validated_data.get("dur")
        wgt = validated_data.get("wgt")
        cmplt = validated_data.get("cmplt")
        return {"rep":rep,"dur":dur,"wgt":wgt,"cmplt":cmplt}


class SessionExerciseListSerializer(serializers.ListSerializer):
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

class SessionExerciseSerializer(serializers.ModelSerializer):
    '''
    Serializer for handling update and creating session exercises
    '''
    id = serializers.UUIDField(required=False)
    sets = serializers.JSONField()

    class Meta:
        model = SessionExercise
        fields = ("id","title","sets","rest_period")
        list_serializer_class = SessionExerciseListSerializer

    def create(self, validated_data):
        workout_session = validated_data.pop("workout_session", None)
        user = validated_data.pop("user", None)
        assert workout_session, "workout session required for creation"
        assert user, "user required for creation"
        title = validated_data.get("title")
        if workout_session is not None and workout_session.exercises.filter(title=title).exists():
            raise serializers.ValidationError({"details":"exercise with this title already exists in workout"})
        exercise = SessionExercise.objects.create(user=user, workout_session=workout_session, **validated_data)
        return exercise

    def update(self, instance, validated_data):
        sets = validated_data.get("sets", [])
        validated_sets = []
        for exercise in sets:
            check = IndividualExerciseSerializer(data=exercise)
            if check.is_valid(raise_exception=True):
                validated_sets.append(check.save())
        validated_data.update({"sets":validated_sets})
        return super().update(instance, validated_data)

class SessionSupersetListSerializer(serializers.ListSerializer):
    '''
    Serializer to handle custom bulk superset update
    '''
    def update(self, queryset, validated_data):
        superset_mapping = {superset.id: superset for superset in queryset}
        data_mapping = {item['id']: item for item in validated_data}
        result = []
        for superset_id, data in data_mapping.items():
            superset = superset_mapping.get(superset_id, None)
            if superset is not None:
                result.append(self.child.update(superset, data))
        return result

class SessionSupersetSerializer(serializers.ModelSerializer):
    '''
    Serializer for handling update and creating session supersets
    '''
    id = serializers.UUIDField(required=False)
    exercises = serializers.JSONField()

    class Meta:
        model = SessionSuperset
        fields = ("id","title","exercises")
        list_serializer_class = SessionSupersetListSerializer

    def create(self, validated_data):
        workout_session = validated_data.pop("workout_session", None)
        user = validated_data.pop("user",None)
        title = validated_data.get("title",None)
        check_duplicates(workout_session, "exercises", title=title,
        err_msg="superset with this title already exists in the workout")
        instance = self.Meta.model(workout=workout_session, user=user, **validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        exercises = validated_data.get("exercises", [])
        validated_exercises = []
        for exercise in exercises:
            validated_sets = []
            for set in exercise.get("sets",[]):
                check = IndividualExerciseSerializer(data=set)
                if check.is_valid(raise_exception=True):
                    validated_sets.append(check.save())
            title = exercise.get("title", instance.title)
            validated_exercises.append({
                "title":title,
                "sets":validated_sets}
                )
        validated_data.update({"exercises":validated_exercises})
        return super().update(instance, validated_data)



class SessionWorkoutDataSerializer(serializers.ModelSerializer):
    '''
    Serializer for workout sessions. Able to create and update a workout session
    '''
    created = serializers.ReadOnlyField(source="workoutSession.created")
    session_exercises = SessionExerciseSerializer(many=True, required=False)
    session_supersets = SessionSupersetSerializer(many=True, required=False)
    class Meta:
        model = WorkoutSession
        fields = (
            "session_exercises","workout_id","created","session_supersets"
        )

    def create(self, validated_data):
        workout_id = validated_data.pop("workout_id", None)
        user = validated_data.pop("user", None)
        assert workout_id, "Workout ID needed to create a workout session"
        assert user, "User needed to create a workout session"
        workout = get_object_or_404(Workout, id=workout_id)
        workoutSession = self.Meta.model.objects.create(workout=workout, user=user, **validated_data)
        return workoutSession

    def update(self, instance, validated_data):
        #* update function capable of updating all branches of the workout session.
        # method should relatively be avoided as cascading udpates may take a bit of time due to 
        # several iterations which grow as the number of exercises and supersets grows
        # this can be seen especially in supersets as the superset updates all of its exercises as well
        partial = validated_data.pop("partial", False)
        session_exercises = validated_data.pop("session_exercises", [])
        session_supersets = validated_data.pop("session_supersets", [])
        # iterate through exercises to update
        for exercise_data in session_exercises:
            exercise_data = dict(**exercise_data)
            exercise = get_object_or_404(SessionExercise, id=exercise_data.get("id"))
            # save the instance using the exercise serializer
            serialized = SessionExerciseSerializer(exercise, data=exercise_data, partial=partial)
            if serialized.is_valid(raise_exception=True):
                serialized.save(workout_session=instance)
        # iterate through supersets
        for superset in session_supersets:
            superset_data = dict(**superset)
            superset = get_object_or_404(SessionSuperset, uuid=superset_data.get("uuid"))
            # save the instance using the superset serializer
            serialized = SessionSupersetSerializer(superset, data=superset_data, partial=partial)
            if serialized.is_valid(raise_exception=True):
                serialized.save(partial=partial)
        return super().update(instance, validated_data)

class TruncatedSessionWorkoutSerializer(serializers.ModelSerializer):
    '''
    Serializer for just viewing workout sessions
    '''
    user = serializers.ReadOnlyField(source="user.id")
    created = serializers.ReadOnlyField(source="workoutSession.created")

    workout_id = serializers.UUIDField(write_only=True)
    class Meta:
        model = WorkoutSession
        fields = (
            "id","title","user","created", "workout_id"
        )

    def create(self, validated_data):
        workout_id = validated_data.pop("workout_id")
        user = validated_data.pop("user", None)
        assert workout_id, "Workout ID needed to create a workout session"
        assert user, "User needed to create a workout session"
        workout = get_object_or_404(Workout, id=workout_id)
        workoutSession = self.Meta.model.objects.create(workout=workout, user=user, **validated_data)
        return workoutSession