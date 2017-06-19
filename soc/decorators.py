from django.core.exceptions import PermissionDenied

def user_has_permission(function):
  def wrap(request, *args, **kwargs):
    print request.user
    return function(request, *args, **kwargs)

