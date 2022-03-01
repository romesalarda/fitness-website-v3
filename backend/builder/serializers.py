from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Category, Superset, Workout, Exercise

from core.utils import set_m2m_using_ids

class CategorySerializer(serializers.ModelSerializer):
    '''Serializer for categories'''
    class Meta:
        model = Category
        fields = ("id","title","description")

class ExerciseSerializer(serializers.ModelSerializer):
    '''serializer for exercises'''

    id = serializers.UUIDField(required=False)
    user = serializers.ReadOnlyField(source="user.id")
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ("id","title","sets","repetitions","duration","public",
        "categories","user","level","target","direction","rest_period","copy_only")

    def create(self, validated_data):
        workout = validated_data.pop("workout", None)
        user = validated_data.pop("user", None)

        title = validated_data.get("title")
        if workout is not None and workout.exercises.filter(title=title).exists():
            raise serializers.ValidationError({"details":"exercise with this title already exists in workout"})
        exercise = Exercise.objects.create(user=user, **validated_data)

        return exercise


class SupersetSerializer(serializers.ModelSerializer):
    '''Serializer for workout supersets'''
    id = serializers.UUIDField(required=False)
    exercises = ExerciseSerializer(many=True, required=False)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Superset
        fields = ("id","title","exercises","public","categories","copy_only")

    def create(self, validated_data):
        # extra fields on save can take in the user and workout for validation and saving
        workout = validated_data.pop("workout", None)
        user = validated_data.pop("user", None)
        title = validated_data.get("title")
        if workout is not None and workout.super_sets.filter(title=title).exists():
            raise serializers.ValidationError({"details":"super set with this title already exists in workout"})
        super_set = Superset.objects.create(user=user, **validated_data)

        return super_set

class WorkoutSerializer(serializers.ModelSerializer):
    '''Serializer for workout'''
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

        if user_workouts is not None and user_workouts.filter(title=validated_data.get("title")).exists():
            raise serializers.ValidationError({"detail":"Workout with that title already exists"})
        workout = self.Meta.model(user=user, **validated_data)
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
                serialized.save()
        # iterate through supersets
        for superset in supersets:
            super_set_data = dict(**superset)
            super_set = get_object_or_404(Superset, id=super_set_data.get("id"))
            # save the instance using the exercise serializer
            serialized = SupersetSerializer(super_set, data=super_set_data, partial=partial)
            if serialized.is_valid(raise_exception=True):
                serialized.save()
        instance.title = validated_data.get("title",instance.title)
        return super().update(instance, validated_data)

class ValidUUIDSerializer(serializers.Serializer):
    '''Serializer used to validate UUID'''
    uuid = serializers.UUIDField()