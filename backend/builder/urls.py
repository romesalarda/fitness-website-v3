from django.urls import path
from .views import (
    WorkoutDestroyUpdateRetrieve,
    WorkoutExercisesView,
    WorkoutListCreate,
)

urlpatterns = [
    path("workouts/", WorkoutListCreate.as_view(), name="workouts"),
    path("workout/<uuid:uuid>/", WorkoutDestroyUpdateRetrieve.as_view(), name="workout-detail"),
    path("workout/<uuid:uuid>/exercises/", WorkoutExercisesView.as_view(), name="workout-exercises"),
   
]
