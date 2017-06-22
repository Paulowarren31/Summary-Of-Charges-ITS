import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import MainForm
from decorators import user_has_permission
from models import um_ecomm_dept_units_rept

from . import database
from django.conf import settings

import requests
import base64
import cx_Oracle #oracle DB lib


connection_string = 'paulowar/'+settings.DB_PASSWORD+'@pinntst.dsc.umich.edu:1521/pinndev.world'

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
      cd = form.cleaned_data
      dept_id = cd.get('dept_id')
      fiscal_yr = cd.get('fiscal_yr')

      #test = um_ecomm_dept_units_rept.objects.filter(deptid=dept_id).filter(fiscal_yr=fiscal_yr)

      #range
      test = um_ecomm_dept_units_rept.objects.filter(deptid__lte=925010, deptid__gte=925000).filter(fiscal_yr=fiscal_yr)

      test = list(test)

      account = test[0].account
      c_grp = test[0].charge_group
      descr = test[0].description

      accounts = {}
      
      total = 0


      #python god
      #TODO
      #this does not work fully 
      for t in test:

        total += floatOrZ(t.unit_rate)
        #if(t.unit_rate is not None or ''):
        if t.account in accounts:

          if t.charge_group in accounts[t.account]:

            if t.description in accounts[t.account][t.charge_group]:

              accounts[t.account][t.charge_group][t.description]['i'].append(t)

              accounts[t.account][t.charge_group][t.description]['total'] += floatOrZ(t.unit_rate)
              accounts[t.account][t.charge_group]['total'] += floatOrZ(t.unit_rate)
              accounts[t.account]['total'] += floatOrZ(t.unit_rate)
            
            else: # new description
              accounts[t.account][t.charge_group][t.description] = {'i': [t], 'total': floatOrZ(t.unit_rate), 'description': t.description}

          else: # new charge group, description
            accounts[t.account][t.charge_group] = {t.description: {'i': [t], 'total': floatOrZ(t.unit_rate), 'description': t.description, 'rate': t.unit_rate, 'bu': t.quantity},'total': floatOrZ(t.unit_rate), 'cg': t.charge_group}

        else: # new account, charge, group, description
          accounts[t.account] = {t.charge_group: {t.description: {'i': [t], 'total': floatOrZ(t.unit_rate), 'description': t.description, 'rate': t.unit_rate, 'bu': t.quantity}, 'total': floatOrZ(t.unit_rate), 'cg': t.charge_group}, 'total': floatOrZ(t.unit_rate), 'acc_desc': t.account_desc}

      for account in accounts.iteritems():
        print account

      return render(request, 'table.html', {'rows': accounts, 'total': total})


    #account{
    #    acc#
    #    acc_descr
    #    total
    #    charge_groups: []
    #    }

    #charge_group{
    #    charge_group
    #    total
    #    descriptions: []
    #    }

    #description{
    #    description
    #    charge_codes
    #    rate
    #    avg_month
    #    billed_units
    #    total
    #    }
      
      #query = "select * from um_ecomm_dept_units_rept where "

      #id_range = cd.get('dept_id_range')
      #d_id = cd.get('dept_id')
      #fiscal_yr = cd.get('fiscal_yr')
      #unit = id_range
      #dateRange = 'Fiscal Year ' + fiscal_yr

      #c = cx_Oracle.connect(connection_string).cursor()


      #if(id_range):
      #  #split dept id range by -
      #  split = id_range.split('-')
      #  begin = split[0]
      #  end = split[1]

      #  print begin, end

      #  query += "deptid between :b and :e and fiscal_yr=:fy" 
      #  print fiscal_yr

      #  rows = c.execute(query, {'b': begin, 'e': end, 'fy': fiscal_yr}).fetchall()
      #  print rows

      #else:
      #  query += "deptid=:d and fiscal_yr=:fy" 
      #  rows = c.execute(query, {'d': d_id, 'fy': fiscal_yr}).fetchall()

      ## currently not being used, but this is how they should be sorted.
      ## sorted by account ID and then by the group name within each account ID
      ## could probably just do the same thing but through SQL, not sure which is faster

      #sort = sorted(rows, cmp=comp)

      ##previous_acc = sort[0][9] # first account id
      ##for row in sort:
      ##  if row[9] != previous_acc:
      ##    #new account
      ##  else:


      ##dictionary that maps account #s to a list of items that belong to that #account
      #account_dict = {}

      #for row in rows:
      #  # row[9] is the account #
      #  if row[9] in account_dict:

      #    account_dict[row[9]].append(row)
      #  else:
      #    account_dict[row[9]] = [row]

      #accounts = account_dict.iteritems() #convert dictionary to list

      #final = {}
      #total = 0
      #months = []
      #m_count = 0


      #for account in accounts:
      #  #dictionary that maps group names to a list of items that belongs to 
      #  #that group
      #  group_dict = {}

      #  account_total = 0
      #  acc_items = account[1] 

      #  for row in acc_items:
      #    g_name = row[11] # group name column
      #    month = row[2]

      #    if month not in months:
      #      months.append(month)
      #      m_count += 1

      #    cost = row[16] # cost column
      #    if g_name in group_dict:
      #      # each group will have a total and a list of items
      #      group_dict[g_name]['items'].append(row)
      #      group_dict[g_name]['total'] += float(cost)
      #    else:
      #      group_dict[g_name] = {'items': [row], 'total': float(cost)}

      #    # sum account total as well
      #    account_total += float(cost)


      #  total += account_total
      #  acc_id = account[0]

      #  final[acc_id] = {'a_total': account_total, 'group_dict': group_dict}

      #


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

def floatOrZ(string):
  try:
    return float(string)
  except:
    return 0.0
