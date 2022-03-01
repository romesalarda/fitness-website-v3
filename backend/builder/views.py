from django.shortcuts import get_object_or_404
# from .utils import filter_queryset, parse_string, order_queryset_by
# # rest
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
# models
from .serializers import (
    WorkoutSerializer,
    SupersetSerializer,
    ExerciseSerializer, 
    ValidUUIDSerializer
)
from api.permission import UserWorkoutAccessPermission
from api.pagination import WorkoutPagination
from .models import Workout, Superset, Exercise, Category

class WorkoutDestroyUpdateRetrieve(APIView):
    '''Delete, update and retrieve a specific user's workout'''
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]

    def get_workout(self):
        uuid = self.kwargs.get("uuid")
        workout = get_object_or_404(Workout, uuid=uuid)
        self.check_object_permissions(self.request, workout)
        return workout

    def get(self, *args, **kwargs):
        workout = self.get_workout()
        serialized = self.serializer_class(workout)
        return Response(serialized.data, status=status.HTTP_200_OK)
   
    def delete(self, *args, **kwargs):
        workout = self.get_workout()
        workout.delete()
        return Response({"detail":"workout deleted"}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, *args, **kwargs):
        workout = self.get_workout()
        serialized = self.serializer_class(workout, data=request.data, partial=True)
        if serialized.is_valid(raise_exception=True):
            serialized.save(partial=True)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class WorkoutListCreate(generics.ListCreateAPIView):
    '''Create and get list of a user's workouts'''
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_workouts(self):
        return Workout.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        workouts = self.get_workouts()

        # search = request.query_params.get("search","")
        # workouts = filter_queryset(workouts,title__contains=search)
        # workouts = self.paginate_queryset(workouts)
        
        serialized = self.serializer_class(workouts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.save(user_workouts=self.get_workouts(), user=request.user)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class WorkoutExercisesView(APIView, WorkoutPagination):
    '''
    Create and add exercises; delete and retrieve exercises and append existing exercises to a workout
    '''
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]   

    def get_workout(self):
        uuid = self.kwargs.get("uuid")
        workout = get_object_or_404(Workout, id=uuid)
        self.check_object_permissions(self.request, workout)
        return workout
    
    def post(self, request, *args, **kwargs):
        # used to create a new exercise and add it to the workout
        workout = self.get_workout()
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid(raise_exception=True):
            new_exercise = serialized.save(workout=workout, user=request.user)
            workout.exercises.add(new_exercise)
            return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # add an already existing exercise to the workout
        workout = self.get_workout()
        serialized = ValidUUIDSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            id = serialized.data.get("uuid")
            exercise = get_object_or_404(Exercise, id=id)
            workout.exercises.add(exercise)
            return Response(status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        # get all exercises of the workout
        workout = self.get_workout()
        exercises = self.paginate_queryset(workout.exercises.all(), request, view=self)
        serialized = self.serializer_class(exercises, many=True)
        return self.get_paginated_response(serialized.data)

    def delete(self, request, *args, **kwargs):
        # remove a exercise from a workout
        workout = self.get_workout()
        serialized = ValidUUIDSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            exercise_id = serialized.data.get("uuid")
            exercise = get_object_or_404(workout.exercises.all(),id=exercise_id)
            workout.exercises.remove(exercise)
            return Response(status=status.HTTP_200_OK)
