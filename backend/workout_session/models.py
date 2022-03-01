from django.conf import settings
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify
from django.core.serializers.json import DjangoJSONEncoder
import uuid
# builder models
from builder.models import Workout


class SessionExercise(models.Model):
    '''
    Used to represent a exercise within a workout session. Contains sets which hold the number of sets of the exercise,
    as well as the duration, repetitons and if it has been completed
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    workout_session = models.ForeignKey("WorkoutSession",on_delete=models.CASCADE, related_name="session_exercises")

    sets = models.JSONField(null=True, encoder=DjangoJSONEncoder, blank=True)
    rest_period = models.FloatField(default=0, blank=True)

    def __str__(self) -> str:
        return "<%s> %s" % (self.workout_session.title, self.title)

class SessionSuperset(models.Model):
    '''
    Used to represent a superset within a workout. The 'exercises' field contains a list of exercises. Each exercise has a title
    and sets which are populated from the host workouts superset exercises.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)

    exercises = models.JSONField(null=True, encoder=DjangoJSONEncoder, blank=True)
    workout_session = models.ForeignKey("WorkoutSession",on_delete=models.CASCADE, related_name="session_supersets", null=True)

    def __str__(self) -> str:
        return "<%s> %s" % (self.workout_session.title, self.title)


class WorkoutSession(models.Model):
    '''
    Simulates the events of a workout session. On creation, uses signals to populate the exercises and
    supersets from the host workout. 
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="workout_sessions", blank=True, null=True)
 
    created = models.DateTimeField(default=timezone.now)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="workout_sessions")

    def __str__(self) -> str:
        return "<session> %s" % self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(WorkoutSession, self).save(*args, **kwargs) 
