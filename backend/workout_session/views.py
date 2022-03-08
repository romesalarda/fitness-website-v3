from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import SessionExerciseSerializer, SessionSupersetSerializer, SessionWorkoutDataSerializer, TruncatedSessionWorkoutSerializer
from .models import SessionExercise, SessionSuperset, WorkoutSession

from api.pagination import WorkoutPagination, SuperSetPagination, ExercisesPagination
from api.permission import UserWorkoutAccessPermission

class WorkoutSessionsView(generics.ListCreateAPIView):
    '''
    Create and retrieve a list of a user's workouts
    '''
    serializer_class = TruncatedSessionWorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_workout_sessions(self):
        return WorkoutSession.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        session_workouts = self.get_workout_sessions()
        # search = request.query_params.get("search","")
        # workouts = filter_queryset(workouts,title__contains=search)
        session_workouts = self.paginate_queryset(session_workouts)

        serialized = self.serializer_class(session_workouts, many=True)
        return self.get_paginated_response(serialized.data)

    def post(self, request, *args, **kwargs):
        serialized = self.serializer_class(data=request.data)
        if serialized.is_valid(raise_exception=True):
            serialized.save(user=request.user)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class SessionExercisesView(APIView, ExercisesPagination):
    '''
    API view to handle retrieval and updating of exercises in a workout session
    '''
    serializer_class = SessionExerciseSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]

    def get_session_exercises(self):
        return SessionExercise.objects.filter(workout_session__id=self.kwargs.get("uuid"))

    def get(self, *args, **kwargs):
        exercises = self.get_session_exercises()
        serialized = self.serializer_class(exercises, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def put(self,request, *args, **kwargs):
        exercises = self.get_session_exercises()
        serialized = self.serializer_class(exercises, data=request.data, many=True)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
        return Response(serialized.data, status=status.HTTP_200_OK)

class SessionSupersetView(APIView, SuperSetPagination):
    '''
    API view to handle retrieval and updating of supersets in a workout session
    '''
    serializer_class = SessionSupersetSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]

    def get_session_supersets(self):
        return SessionSuperset.objects.filter(workout_session__id=self.kwargs.get("uuid"))

    def get(self, request, *args, **kwargs):
        supersets = self.get_session_supersets()
        serialized = self.serializer_class(self.paginate_queryset(supersets), many=True)

        return self.get_paginated_response(serialized.data)

    def put(self,request, *args, **kwargs):
        supersets = self.get_session_supersets()
        serialized = self.serializer_class(supersets, data=request.data, many=True)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
        return Response(serialized.data, status=status.HTTP_200_OK)

class SessionDetailView(generics.RetrieveDestroyAPIView, WorkoutPagination):
    '''
    API view to handle the retrieval and deletion of a workout session
    '''
    serializer_class = SessionWorkoutDataSerializer
    permission_classes = [permissions.IsAuthenticated, UserWorkoutAccessPermission]

    def get_object(self):
        session = get_object_or_404(WorkoutSession, id=self.kwargs.get("uuid"))
        self.check_object_permissions(self.request, session)
        return session

    