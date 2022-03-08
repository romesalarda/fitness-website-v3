from django.urls import path

from .views import *
urlpatterns = [
    # view general workout sessions
    path("workout-sessions/", WorkoutSessionsView.as_view(),name="workout-sessions"),

    path("workout-session/<uuid:uuid>/exercises/", SessionExercisesView.as_view() ,name="workout-session-exercises"),
    path("workout-session/<uuid:uuid>/supersets/", SessionSupersetView.as_view() ,name="workout-session-supersets"),
    path("workout-session/<uuid:uuid>/detail/", SessionDetailView.as_view() ,name="workout-session-detail"),
]
