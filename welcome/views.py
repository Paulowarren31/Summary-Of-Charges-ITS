import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import MyForm

from . import database

import requests
import base64
import cx_Oracle #oracle DB lib

#ayy lmaoooooooo

try:
  with open('/usr/src/app/myapp/local/oracle/password', 'rb') as f:
    db_pass = f.read()
  #connection_string = 'paulowar/'+db_pass+'@pinntst.dsc.umich.edu:1521/pinndev.world'
except:
  print 'error reading secret'

#@login_required(login_url='/accounts/login')
def index(request):
  dic = {}

  conn = cx_Oracle.connect(connection_string)
  cursor = conn.cursor()

  query = "select * from um_ecomm_dept_units_rept where ROWID IN ( SELECT MAX(ROWID) FROM um_ecomm_dept_units_rept GROUP BY dept_grp)"

  dic['dept_grp'] = cursor.execute(query).fetchall()

  query = "select * from um_ecomm_dept_units_rept where ROWID IN ( SELECT MAX(ROWID) FROM um_ecomm_dept_units_rept GROUP BY dept_grp_vp_area)"

  vp_area = cursor.execute(query).fetchall()

  dic['vp'] = vp_area

  query = "select * from um_ecomm_dept_units_rept where ROWID IN ( SELECT MAX(ROWID) FROM um_ecomm_dept_units_rept GROUP BY dept_bud_seq)"

  budget_seq = cursor.execute(query).fetchall()

  dic['bud_seq'] = budget_seq

  form = MyForm()
  dic['form'] = form

  conn.close()

  return render(request, 'index.html', dic)

#@login_required(login_url='/accounts/login')
def table(request):

  form = MyForm()
  if request.method == 'POST':
    form = MyForm(request.POST)

    if form.is_valid():
      cd = form.cleaned_data
      id_range = cd.get('dept_id_range').split('-')
      minimum = id_range[0]
      maximum = id_range[1]

      fiscal_yr = cd.get('fiscal_yr')

      query = "select * from um_ecomm_dept_units_rept where "
      query += "deptid between %s and %s and fiscal_yr=%s" % (minimum, maximum, fiscal_yr)


      conn = cx_Oracle.connect(connection_string)
      cursor = conn.cursor()

      rows = cursor.execute(query).fetchall()

      #dictionary that maps account #s to a list of items that belong to that account
      account_dict = {}

      for row in rows:
        if row[9] in account_dict:
          account_dict[row[9]].append(row)
        else:
          account_dict[row[9]] = [row]

      accounts = account_dict.iteritems()

      final = {}

      for account in accounts:
        #dictionary that maps group names to a list of items that belongs to that group
        group_dict = {}
        account_total = 0
        for row in account[1]:
          if row[11] in group_dict:
            group_dict[row[11]]['items'].append(row)
            group_dict[row[11]]['total'] += float(row[16])
          else:
            group_dict[row[11]] = {'items': [row], 'total': float(row[16])}

          account_total += float(row[16])


        final[account[0]] = {'a_total': account_total, 'group_dict': group_dict}


      return render(request, 'table.html', {"rows": final})



    #query = "select * from um_ecomm_dept_units_rept where "

    #type1 = int(request.POST['type1'])

    #  maximum = request.POST['max']

    #  query += "deptid between %s and %s " % (minimum, maximum)

    #elif type1 == 2:
    #  pass
    #elif type1 == 3:
    #  pass
    #else:
    #  print('error')

    #type2 = int(request.POST['type2'])

    #if type2 == 0:
    #  f_yr = request.POST['fiscal_yr']

    #  query += "and fiscal_yr=%s" % f_yr
    #  pass
    #elif type2 == 1:
    #  pass
    #elif type2 == 2:
    #  pass
    #elif type2 == 3:
    #  pass
    #else:
    #  print('error')



def profile(request):
  return render(request, 'index.html')
