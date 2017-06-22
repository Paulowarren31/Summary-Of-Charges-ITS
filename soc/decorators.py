from django.core.exceptions import PermissionDenied
from django.conf import settings
import cx_Oracle

def user_has_permission(function):
  connection_string = 'paulowar/'+settings.DB_PASSWORD+'@pinntst.dsc.umich.edu:1521/pinndev.world'
  def wrap(request, *args, **kwargs):
    print request.user.username

    c = cx_Oracle.connect(connection_string).cursor()
    query = 'select * from um_authorized_dept_users where uniqname=:u'
    result = c.execute(query, {'u': request.user.username}).fetchall()

    print result

    if len(result) == 0:
      raise PermissionDenied
    else:
      return function(request, *args, **kwargs)
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap
