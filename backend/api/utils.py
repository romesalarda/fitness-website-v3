from rest_framework.serializers import ValidationError
from django.db.models.manager import BaseManager
from django.db.models.query import QuerySet
from django.db.models import Model

def check_duplicates(instance_or_queryset:Model|QuerySet, manager:BaseManager|str=None, err_msg=None, **kwargs):
    '''
    Check duplicates in model or queryset. Manager can either be the manager of the instance or a string
    which points to the manager on the instance. If a duplicate item is found, a serializer validation
    error is raised
    '''
    if instance_or_queryset is None:
        return None
    # if the manager is not given, query the instance as if it were a queryset.
    if isinstance(instance_or_queryset, QuerySet):
        obj = instance_or_queryset
    # if there is a manager, check if it is a manager, if not, try and get the manager using
    # a name
    elif not isinstance(manager, BaseManager):
        assert manager is not None, "Manger required if queryset not provided"
        obj = getattr(instance_or_queryset, manager, None)
        assert obj is not None, "Manager not found"
    else:
        raise TypeError("Expected queryset or manager")

    if obj.filter(**kwargs).exists():
        raise ValidationError({"details":err_msg})
    return True