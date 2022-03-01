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