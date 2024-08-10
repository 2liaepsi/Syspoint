from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def responsable_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Responsables').exists() or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap