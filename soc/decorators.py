from django.core.exceptions import PermissionDenied
from django.conf import settings
from models import Authorized_User
import cx_Oracle

def user_has_permission(function):

  def wrap(request, *args, **kwargs):

    query = Authorized_User.objects.filter(uniqname=request.user.username)

    if len(query) != 0 or request.user.is_superuser or request.user.username == 'djamison' or request.user.username == 'rutag':
      return function(request, *args, **kwargs)
    else:
      raise PermissionDenied

  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap
