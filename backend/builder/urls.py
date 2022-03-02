from django.urls import path
from .views import *

urlpatterns = [
    # for user to view all their workouts
    path("workouts/", 
    WorkoutsView.as_view(), 
    name="workouts"),
    # allows user to delete, update and retrieve a specific workout
    path("workout/<uuid:uuid>/", 
    WorkoutDetailView.as_view(), 
    name="workout-detail"),
    # allows user to create, add and retrieve exercises
    path("workout/<uuid:uuid>/exercises/", 
    WorkoutExercisesView.as_view(), 
    name="workout-exercises"),
    # allows user to delete, update and retrieve a specific exercise in the workout
    path("workout/<uuid:uuid>/exercise/<uuid:exerciseid>/", 
    WorkoutExerciseDetailView.as_view(), 
    name="workout-exercise-detail"),
    # allows uer to create, add and retrieve supersets in a workout
    path("workout/<uuid:uuid>/supersets/", 
    WorkoutSupersetsView.as_view(), 
    name="workout-supersets"),
    # view to retrieve, update and delete a specific superset
    path("workout/<uuid:uuid>/superset/<uuid:supersetid>/", 
    WorkoutSupersetDetailView.as_view(), 
    name="workout-superset-detail"),
    # Create, add, and retrieve exercises and append existing exercises to a superset
    path("workout/<uuid:uuid>/superset/<uuid:supersetid>/exercises/", 
    WorkoutSupersetExercisesView.as_view(), 
    name="workout-superset-exercises"),
    # View to retrieve, update, and delete a specific superset. 
    # Also able to add exercises using the put request.
    path("workout/<uuid:uuid>/superset/<uuid:supersetid>/exercise/<uuid:exerciseid>/", 
    WorkoutSupersetExercisesDetailView.as_view(), 
    name="workout-superset-exercise-detail"),
    # special search querying for exercises
    path("exercises/", 
    ExerciseQueryView.as_view(), 
    name="query-exercises")

]
