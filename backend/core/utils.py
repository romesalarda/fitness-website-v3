from rest_framework import serializers

def set_m2m_using_ids(model, iterable, callback, error_msg=None):
    '''
    update an instance m2m field by filtering the global models by ID.

    model: global model
    
    iterable: iterable of ids 

    instance callback: model.<m2mfield>.set(queryset)
    '''
    try:
        if iterable:
            queryset = model.objects.filter(id__in=iterable)
            return callback(queryset)
    except Exception:
        raise serializers.ValidationError({"detail":error_msg})

from django.db.models import Q

# contains querying utils to avoid error raising when querying
# generally, a failed query will just return the queryset instead of raising an error
def parse_string(string, sep=","):
    '''
    Convert a string to a list of integers by specifying separators.

    If there as a non-integer, returns False
    '''
    if not string:
        return []
    try: 
        split = string.strip().split(sep)
        return list(map(int, split))
    except Exception:
        return False

def filter_queryset(queryset, **kwargs):
    '''
    Build conditions if their values are not none then filter.

    If there are no conditions, returns original queryset
    '''
    conditions = tuple([Q((key, value)) for key, value in kwargs.items() if value])
    if conditions:
        return queryset.filter(*conditions)
    return queryset

def order_queryset_by(value, queryset):
    '''
    Order queryset by value. If value does not exist, original queryset is returned
    '''
    if not value:
        return queryset
    value = value.strip()
    try:
        return queryset.order_by(value)
    except Exception:
        return queryset