from django.shortcuts import get_object_or_404
from .models import Workout

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