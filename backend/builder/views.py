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
    UUIDSerializer
)
from api.permission import UserWorkoutAccessPermission
from api.pagination import ExercisesPagination, SuperSetPagination, WorkoutPagination

from .models import Workout, Superset, Exercise, Category

from core.utils import parse_string, filter_queryset, order_queryset_by

class RetrieveWorkoutMixin:
    '''
    Mixin for retrieving the specified workout using a UUID. Checks permissions after fetch
    '''
    def get_workout(self):
        uuid = self.kwargs.get("uuid")
        workout = get_object_or_404(Workout, id=uuid)
        self.check_object_permissions(self.request, workout)
        return workout

class RetrieveSupersetWorkoutMixin(RetrieveWorkoutMixin):
    '''
    Mixin for retrieving the specified superset using a UUID. Checks permissions after fetch
    '''
    def get_superset(self):
        workout = self.get_workout()
        superset_id = self.kwargs.get("supersetid")
        superset = get_object_or_404(workout.supersets.all(), id=superset_id)
        return superset

class WorkoutDetailView(APIView, RetrieveWorkoutMixin):
    '''
    Delete, update and retrieve a specific user's workout
    '''
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]

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

class WorkoutsView(generics.ListCreateAPIView):
    '''
    Create and retrieve a list of a user's workouts
    '''
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

class WorkoutExercisesView(APIView, RetrieveWorkoutMixin, WorkoutPagination):
    '''
    Create, add, and retrieve exercises and append existing exercises to a workout
    '''
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]   
    
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
        serialized = UUIDSerializer(data=request.data)
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

class WorkoutExerciseDetailView(APIView, RetrieveWorkoutMixin, ExercisesPagination):

    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]   

    def get_exercise(self):
        workout = self.get_workout()
        exercise_id = self.kwargs.get("exerciseid")
        exercise = get_object_or_404(workout.exercises.all(), id=exercise_id)
        return exercise
    
    def get(self, request, *args, **kwargs):
        # get superset data of a workout
        exercise = self.get_exercise()
        serialized = self.serializer_class(exercise)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        # update exercise
        exercise = self.get_exercise()
        serialized = self.serializer_class(exercise, data=request.data, partial=True)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # remove superset from workout
        exercise = self.get_exercise()  
        self.get_workout().exercises.remove(exercise)
        return Response(status=status.HTTP_204_NO_CONTENT)



class WorkoutSupersetsView(APIView, RetrieveWorkoutMixin, SuperSetPagination):
    '''
    Create, add and retrieve supersets and append existing supersets to a workout
    '''
    serializer_class = SupersetSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]   

    def post(self, request, *args, **kwargs):
        # used to create a new superset and add it to the workout
        workout = self.get_workout() 
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid(raise_exception=True):
            super_set = serialized.save(workout=workout, user=request.user)
            workout.supersets.add(super_set)
            return Response(status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        # add an already existing superset to the workout
        workout = self.get_workout()
        serialized = UUIDSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            id = serialized.data.get("uuid")
            super_set = get_object_or_404(Superset, id=id)
            workout.supersets.add(super_set)
            return Response(status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        # get all supersets of the workout
        workout = self.get_workout()
        supersets = self.paginate_queryset(workout.supersets.all(), request, view=self)
        serialized = self.serializer_class(supersets, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

class WorkoutSupersetDetailView(APIView, RetrieveSupersetWorkoutMixin):
    '''
    View to retrieve, update, and delete a specific superset. Also able to add exercises using the 
    put request.
    '''
    serializer_class = SupersetSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission] 

    
    def get(self, *args, **kwargs):
        # get superset data of a workout
        super_set = self.get_superset()
        serialized = self.serializer_class(super_set)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # add an existing exercise to a superset
        serialized = UUIDSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            superset = self.get_superset()
            exercise = get_object_or_404(Exercise, id=serialized.data.get("exercise_id"))
            superset.exercises.add(exercise)
            return Response(status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        # update entire superset
        superset = self.get_superset()
        serialized = self.serializer_class(superset, data=request.data, partial=True)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        # remove superset from workout
        superset = self.get_superset()  
        self.get_workout().supersets.remove(superset)
        return Response(status=status.HTTP_204_NO_CONTENT)

class WorkoutSupersetExercisesView(APIView, RetrieveSupersetWorkoutMixin, WorkoutPagination):
    '''
    Create, add, and retrieve exercises and append existing exercises to a superset
    '''
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]   
    
    def post(self, request, *args, **kwargs):
        # used to create a new exercise and add it to the superset
        superset = self.get_superset()
        workout = self.get_workout()
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid(raise_exception=True):
            new_exercise = serialized.save(workout=workout, user=request.user)
            superset.exercises.add(new_exercise)
            return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # add an already existing exercise to the superset
        superset = self.get_superset()
        serialized = UUIDSerializer(data=request.data)
        if serialized.is_valid(raise_exception=True):
            id = serialized.data.get("uuid")
            exercise = get_object_or_404(Exercise, id=id)
            superset.exercises.add(exercise)
            return Response(status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        # get all exercises of the superset
        superset = self.get_superset()
        exercises = self.paginate_queryset(superset.exercises.all(), request, view=self)
        serialized = self.serializer_class(exercises, many=True)
        return self.get_paginated_response(serialized.data)

class WorkoutSupersetExercisesDetailView(APIView, RetrieveSupersetWorkoutMixin):
    '''
    View to retrieve, update, and delete a specific superset. Also able to add exercises using the 
    put request.
    '''
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission] 

    def get_exercise(self):
        exercise_id = self.kwargs.get("exerciseid")
        superset = self.get_superset()
        exercise = get_object_or_404(superset.exercises.all(), id=exercise_id)
        return exercise
    
    def get(self, *args, **kwargs):
        # get superset data of a workout
        exercise = self.get_exercise()
        serialized = self.serializer_class(exercise)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        # update superset exercise
        exercise = self.get_exercise()
        serialized = self.serializer_class(exercise, data=request.data, partial=True)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        # remove exercise from superset
        exercise = self.get_exercise()  
        self.get_superset().exercises.remove(exercise)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExerciseQueryView(APIView, ExercisesPagination):
   
    # has the get method that supports special querying for searches
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]   

    only_allow_public = None
            
    def get(self, request, *args, **kwargs):
        # get list of all exercises
        search = request.query_params.get("search","")
        exercises = Exercise.objects.filter(title__contains=search, user=request.user)
        # get extra params
        level = request.query_params.get("level","")
        direction = request.query_params.get("direction","")
        target = request.query_params.get("target","")
        categories = request.query_params.get("categories", None)
        orderby = request.query_params.get("order", None)
        # filter 
        exercises = filter_queryset(queryset = exercises, 
        categories__in=parse_string(categories),
        direction__in=parse_string(direction),
        target__in=parse_string(target),
        level__in=parse_string(level),
        public=self.only_allow_public
        )
        exercises = order_queryset_by(orderby, exercises)
        # paginate
        exercises = self.paginate_queryset(exercises, request, view=self)
        serialized = self.serializer_class(exercises, many=True)
        return self.get_paginated_response(serialized.data)
