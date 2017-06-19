import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import MainForm

from . import database

import requests
import base64
import cx_Oracle #oracle DB lib


# Should this go somewhere else?

try:
  #try and open DB password file mounted by openshift
  with open('/usr/src/app/myapp/local/oracle/password', 'rb') as f:
    db_pass = f.read()
  connection_string = 'paulowar/'+db_pass+'@pinntst.dsc.umich.edu:1521/pinndev.world'
except:
  print 'error reading DB secret'


# index view
@login_required(login_url='/accounts/login')
def index(request):
  res = {}

  conn = cx_Oracle.connect(connection_string)
  cursor = conn.cursor()

  #select all of the unique dept_grps 
  query = "select * from um_ecomm_dept_units_rept where ROWID IN ( SELECT MAX(ROWID) FROM um_ecomm_dept_units_rept GROUP BY dept_grp)"

  res['dept_grps'] = cursor.execute(query).fetchall()

  #select all of the unique dept_grp_vp_areas 
  query = "select * from um_ecomm_dept_units_rept where ROWID IN ( SELECT MAX(ROWID) FROM um_ecomm_dept_units_rept GROUP BY dept_grp_vp_area)"

  res['vp_areas'] = cursor.execute(query).fetchall()

  #select all of the unique dept_bud_seqs
  query = "select * from um_ecomm_dept_units_rept where ROWID IN ( SELECT MAX(ROWID) FROM um_ecomm_dept_units_rept GROUP BY dept_bud_seq)"

  res['bud_seqs'] = cursor.execute(query).fetchall()

  conn.close()

  res['form'] = MainForm()

  return render(request, 'index.html', res)

# table view
@login_required(login_url='/accounts/login')
def table(request):

  form = MainForm()
  # if coming from index 
  if request.method == 'POST':
    # create form obj with post params
    form = MainForm(request.POST)
    
    if form.is_valid():
      cd = form.cleaned_data
      #split dept id range by -
      id_range = cd.get('dept_id_range').split('-')
      minimum = id_range[0]
      maximum = id_range[1]

      fiscal_yr = cd.get('fiscal_yr')

      query = "select * from um_ecomm_dept_units_rept where "
      query += "deptid between :b and :e and fiscal_yr=:fy" 

      print query

      cursor = cx_Oracle.connect(connection_string).cursor()

      rows = cursor.execute(query, {'b': minimum, 'e': maximum, 'fy': fiscal_yr}).fetchall()

      #dictionary that maps account #s to a list of items that belong to that account
      account_dict = {}

      for row in rows:
        # row[9] is the account #
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
        acc_items = account[1]

        for row in acc_items:
          #row[11] is group name
          g_name = row[11]
          cost = row[16]
          if g_name in group_dict:
            # each group will have a total and a list of items
            group_dict[g_name]['items'].append(row)
            group_dict[g_name]['total'] += float(cost)
          else:
            group_dict[g_name] = {'items': [row], 'total': float(cost)}

          # sum account total as well
          account_total += float(cost)


        acc_id = account[0]
        final[acc_id] = {'a_total': account_total, 'group_dict': group_dict}


      return render(request, 'table.html', {"rows": final})
