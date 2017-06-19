from django.core.exceptions import PermissionDenied
import cx_Oracle

def user_has_permission(function):
  def wrap(request, *args, **kwargs):
    try:
      #try and open DB password file mounted by openshift
      with open('/usr/src/app/myapp/local/oracle/password', 'rb') as f:
        db_pass = f.read()
      connection_string = 'paulowar/'+db_pass+'@pinntst.dsc.umich.edu:1521/pinndev.world'
    except:
      connection_string = 'paulowar/Pw6517nP@pinntst.dsc.umich.edu:1521/pinndev.world'

    print request.user.username

    c = cx_Oracle.connect(connection_string).cursor()
    query = 'select * from um_authorized_dept_users where uniqname=:u'
    result = c.execute(query, {'u': request.user.username})

    print result

    if len(result) == 0:
      raise PermissionDenied
    else:
      return function(request, *args, **kwargs)
  wrap.__doc__ = function.__doc__
  wrap.__name__ = function.__name__
  return wrap
