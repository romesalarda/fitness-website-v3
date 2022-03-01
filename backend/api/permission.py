from rest_framework import permissions

class UserWorkoutAccessPermission(permissions.BasePermission):
    # Restricts access to a view no matter which type of request is sent
    message = 'Access denied'

    def has_object_permission(self, request, view, obj, *args, **kwargs):
        return obj.user == request.user
