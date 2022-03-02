from django.urls import path
from .views import *

urlpatterns = [
    path("workouts/", 
    WorkoutsView.as_view(), 
    name="workouts"),

    path("workout/<uuid:uuid>/", 
    WorkoutDetailView.as_view(), 
    name="workout-detail"),

    path("workout/<uuid:uuid>/exercises/", 
    WorkoutExercisesView.as_view(), 
    name="workout-exercises"),

    path("workout/<uuid:uuid>/exercise/<uuid:exerciseid>/", 
    WorkoutExerciseDetailView.as_view(), 
    name="workout-exercise-detail"),
    
    path("workout/<uuid:uuid>/supersets/", 
    WorkoutSupersetsView.as_view(), 
    name="workout-supersets"),

    path("workout/<uuid:uuid>/superset/<uuid:supersetid>/", 
    WorkoutSupersetDetailView.as_view(), 
    name="workout-superset-detail"),
   
    path("workout/<uuid:uuid>/superset/<uuid:supersetid>/exercises/", 
    WorkoutSupersetExercisesView.as_view(), 
    name="workout-superset-exercises"),
    
    path("workout/<uuid:uuid>/superset/<uuid:supersetid>/exercise/<uuid:exerciseid>/", 
    WorkoutSupersetExercisesDetailView.as_view(), 
    name="workout-superset-exercise-detail"),

    path("exercises/", 
    ExerciseQueryView.as_view(), 
    name="query-exercises")

]
