import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from . import database

import requests
import base64
import cx_Oracle #oracle DB lib

connection_string = 'paulowar/Pw6517nP@pinntst.dsc.umich.edu:1521/pinndev.world'

# Create your views here.

@login_required(login_url='/accounts/login')
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


  conn.close()

  return render(request, 'index.html', dic)

#@login_required(login_url='/accounts/login')
def table(request):

  conn = cx_Oracle.connect(connection_string)
  cursor = conn.cursor()

  query = "select * from um_ecomm_dept_units_rept where deptid='926200' and month='01' and calendar_yr='2015'"

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

  return render(request, 'table.html', {'rows': final})

def secret(request):
  with open('/usr/src/app/myapp/local/saml/secret-key', 'rb') as f:
    secret_key = str(base64.b64encode(f.read()), 'utf-8')
    return render(request, 'secret.html', {'key': secret_key})

def profile(request):
  return render(request, 'index.html')
