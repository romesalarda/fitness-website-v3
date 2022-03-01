from django.contrib import admin

from workout_session.models import SessionExercise, SessionSuperset, WorkoutSession

# Register your models here.
admin.site.register(WorkoutSession)
admin.site.register(SessionExercise)
admin.site.register(SessionSuperset)
