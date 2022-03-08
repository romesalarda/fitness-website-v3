
from django.dispatch import receiver
from django.db.models.signals import post_save

from builder.models import Superset

from .models import WorkoutSession, SessionExercise, SessionSuperset

@receiver(post_save, sender=WorkoutSession)
def populate_session(sender, instance, created, **kwargs):
    '''
    Signal used to populate the exercises and supersets of a session so that
    it is ready for the frontend. Only run on creation of a workout session.
    '''
    if created:
        exercise_targets = ("title","sets","repetitions","duration","weight","rest_period")
        workout = instance.workout
        # populate exercises
        for exercise in workout.exercises.all().values(*exercise_targets):
            print(exercise)
            sets = exercise.pop("sets")
            populate_data = {
                "rep":exercise.pop("repetitions"),
                "dur":exercise.pop("duration"),
                "wgt":exercise.pop("weight"),
                "cmplt":False
            }
            populated_sets = [populate_data for _ in range(sets)]
            SessionExercise.objects.create(sets=populated_sets, workout_session=instance, **exercise)
        # populate supersets
        superset_targets = ("title","sets","repetitions","duration")
        for superset in workout.supersets.all():
            exercises = superset.exercises.values(*superset_targets)
            result = []
            # for each exercise, create a dictionary with the title and sets as a list populated
            for exercise in exercises:
                sets = exercise.get("sets")
                print(sets)
                populate_data = {
                    "rep":exercise.get("repetitions"),
                    "dur":exercise.get("duration"), 
                    "wgt":exercise.get("weight"),
                    "cmplt":False
                }
                populated_sets = [populate_data for _ in range(sets)]
                result.append({"title":exercise.get("title"), "sets":populated_sets})
            SessionSuperset.objects.create(workout_session=instance, title=superset.title, exercises=result)
        
