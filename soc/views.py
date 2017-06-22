import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import MainForm
from decorators import user_has_permission
from models import um_ecomm_dept_units_rept
from . import database

import requests
import base64
import cx_Oracle #oracle DB lib

# Should this go somewhere else?

#python decouple

try:
  #try and open DB password file mounted by openshift
  with open('/usr/src/app/myapp/local/oracle/password', 'rb') as f:
    db_pass = f.read()
  connection_string = 'paulowar/'+db_pass+'@pinntst.dsc.umich.edu:1521/pinndev.world'
except:
  connection_string = 'paulowar/Pw6517nP@pinntst.dsc.umich.edu:1521/pinndev.world'
  print 'error reading DB secret'


# index view
#@login_required(login_url='/accounts/login')
# uniqname must be in the pinnacle authorized users table
#@user_has_permission
def index(request):

  test =  list(um_ecomm_dept_units_rept.objects.filter(month='06').filter(deptid='925010'))
  print test[0]

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
#@login_required(login_url='/accounts/login')
def table(request):

  form = MainForm()
  # if coming from index 
  if request.method == 'POST':
    # create form obj with post params
    form = MainForm(request.POST)
    
    if form.is_valid():
      query = "select * from um_ecomm_dept_units_rept where "

      cd = form.cleaned_data
      id_range = cd.get('dept_id_range')
      d_id = cd.get('dept_id')
      fiscal_yr = cd.get('fiscal_yr')
      unit = id_range
      dateRange = 'Fiscal Year ' + fiscal_yr

      c = cx_Oracle.connect(connection_string).cursor()


      if(id_range):
        #split dept id range by -
        split = id_range.split('-')
        begin = split[0]
        end = split[1]

        print begin, end

        query += "deptid between :b and :e and fiscal_yr=:fy" 
        print fiscal_yr

        rows = c.execute(query, {'b': begin, 'e': end, 'fy': fiscal_yr}).fetchall()
        print rows

      else:
        query += "deptid=:d and fiscal_yr=:fy" 
        rows = c.execute(query, {'d': d_id, 'fy': fiscal_yr}).fetchall()

      # currently not being used, but this is how they should be sorted.
      # sorted by account ID and then by the group name within each account ID
      # could probably just do the same thing but through SQL, not sure which is faster
      sort = sorted(rows, cmp=comp)

      #previous_acc = sort[0][9] # first account id
      #for row in sort:
      #  if row[9] != previous_acc:
      #    #new account
      #  else:


      #dictionary that maps account #s to a list of items that belong to that #account
      account_dict = {}

      for row in rows:
        # row[9] is the account #
        if row[9] in account_dict:

          account_dict[row[9]].append(row)
        else:
          account_dict[row[9]] = [row]

      accounts = account_dict.iteritems() #convert dictionary to list

      final = {}
      total = 0



      for account in accounts:
        #dictionary that maps group names to a list of items that belongs to 
        #that group
        group_dict = {}

        account_total = 0
        acc_items = account[1] 

        for row in acc_items:
          g_name = row[11] # group name column

          cost = row[16] # cost column
          if g_name in group_dict:
            # each group will have a total and a list of items
            group_dict[g_name]['items'].append(row)
            group_dict[g_name]['total'] += float(cost)
          else:
            group_dict[g_name] = {'items': [row], 'total': float(cost)}

          # sum account total as well
          account_total += float(cost)


        total += account_total
        acc_id = account[0]

        final[acc_id] = {'a_total': account_total, 'group_dict': group_dict}

      

      return render(request, 'table.html', {'rows': final, 'total': total, 
        'unit': unit, 'dateRange': dateRange})

def comp(a, b):
  a_id = int(a[9]) #account ids
  b_id = int(b[9])

  if a_id == b_id:
    a_grp = a[11] #group names
    b_grp = b[11]

    if a_grp < b_grp:
      return 1
    else:
      return -1
  else:
    return a_id - b_id



