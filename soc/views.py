import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import MainForm
from decorators import user_has_permission
from models import um_ecomm_dept_units_rept
from django.db import models
from django.http import JsonResponse

from . import database
from django.conf import settings

import requests
import base64



# index view
@login_required(login_url='/accounts/login')
#uniqname must be in the pinnacle authorized users table
@user_has_permission
def index(request):
  res = {}
  res['form'] = MainForm()

  return render(request, 'index.html', res) 

@login_required(login_url='/accounts/login')
@user_has_permission
def dept_info(request):
  if request.method == 'POST':

    dept_ids =  request.POST.dict()['dept_ids']
    print dept_ids

    query = handleDeptQuery(dept_ids).order_by().values_list('deptid','dept_descr').distinct()

    dept_list = list(query)

    print dept_list

    return JsonResponse({'list': dept_list})

# table view
@login_required(login_url='/accounts/login')
@user_has_permission
def table(request):

  print 'table'
  form = MainForm()
  # if coming from index
  if request.method == 'POST':
    print 'post'
    # create form obj with post params
    form = MainForm(request.POST)

    if form.is_valid():
      print 'clean form'

      cd = form.cleaned_data
      date_range = ''
      unit = ''

      choice2 = int(cd.get('t_choice'))

      print choice2

      
      #if choice1 == 1:
      #  dept_id = cd.get('dept_id')

      #  unit = 'Dept id: ' + dept_id
      #  query = um_ecomm_dept_units_rept.objects.filter(deptid=dept_id)

      #  query2 = query.filter(calendar_yr='2015').filter(month='1')
      #  print 'trying debug query'
      #  print list(query2)

      dept_range = cd.get('dept_id_range')

      unit = 'Dept ids: ' + dept_range

      query = handleDeptQuery(dept_range)

      if choice2 == 1:
        fiscal_yr = cd.get('fiscal_yr')

        query = query.filter(fiscal_yr=fiscal_yr)
        date_range = 'Fiscal year ' + fiscal_yr

      elif choice2 == 2:
        calendar_yr = cd.get('calendar_yr')

        date_range = 'Calendar year ' + calendar_yr
        query = query.filter(calendar_yr=calendar_yr)

      #elif choice2 == 8:
      #  month = cd.get('single_month_m')
      #  year = cd.get('single_month_y')

      #  print 'single month'
      #  print month
      #  print year

      #  date_range = month + ' / ' + year

      #  if len(month) == 1:
      #    month = month.zfill(2)

      #  query = query.filter(calendar_yr=year).filter(month=month)

      elif choice2 == 3:
        b_month = cd.get('range_begin_m')

        if len(b_month) == 1:
          b_month = b_month.zfill(2)

        b_year = cd.get('range_begin_y')

        e_month = cd.get('range_end_m')

        if len(e_month) == 1:
          e_month = e_month.zfill(2)

        e_year = cd.get('range_end_y')

        date_range = b_month + ' ' + b_year + ' to ' + e_month + ' ' + e_year

        b_query = query.filter(calendar_yr__gte=b_year, month__gte=b_month)
        e_query = query.filter(calendar_yr__lte=e_year, month__lte=e_month)
        query = b_query.intersection(e_query)

      rows = list(query.distinct())

      accounts, total = handleAccounts(rows)

      for acc in accounts:
        acc['items'] = handleGroups(acc)
        for group in acc['items']:
          group['items'] = handleDescriptions(group)

      form.save(unit, date_range) # save what they searched for

      print accounts

      return render(request, 'table.html', {'accounts': accounts, 'total': total, 'unit': unit, 'dateRange': date_range})

    else:
      print form.errors
      return render(request, 'index.html', {'form': form})

  else: #if not POST request
    return render(request, 'index.html', {'form': form})

# tries to convert a string to a float, returns 0 if exception
def floatOrZ(string):
  try:
    return float(string)
  except:
    return 0.0

#gives back array of items grouped by their account
def handleAccounts(items):
  accounts = []
  t_total = 0
  p = ''
  for i in items:
    t_total += floatOrZ(i.amount)
    if i.account != p or p == '':
      a = {'items': [i], 'desc': i.account_desc, 'num': i.account, 'total': floatOrZ(i.amount)}
      accounts.append(a)
    else:
      accounts[-1]['items'].append(i)
      accounts[-1]['total'] += floatOrZ(i.amount)
    p = str(i.account)

  return (accounts,t_total)

def handleGroups(account):
  groups = []
  g_total = 0
  c = ''
  for i in account['items']:
    if i.charge_group != c or c == '':
      cg = {'items': [i], 'code': i.charge_code,'grp': i.charge_group, 'total': floatOrZ(i.amount)}
      groups.append(cg)
    else:
      groups[-1]['items'].append(i)
      groups[-1]['total'] += floatOrZ(i.amount)
    c = i.charge_group

  return groups


def handleDescriptions(group):
  descs = []
  d_total = 0
  d = ''


  for i in group['items']:
    if i.description != d or d == '':
      descr = {'items': [i], 'cc': i.charge_code, 'unit_rate': i.unit_rate, 'quantity': floatOrZ(i.quantity), 'total': floatOrZ(i.amount), 'descr': i.description, 'months': [i.month], 'm_count': 1}

      descs.append(descr)
    else:
      descs[-1]['items'].append(i)
      descs[-1]['quantity'] += floatOrZ(i.quantity)
      descs[-1]['total'] += floatOrZ(i.amount)

      if i.month not in descs[-1]['months']:
        descs[-1]['m_count'] += 1
        descs[-1]['months'].append(i.month)

    d = i.description

  for d in descs:
    d['monthly'] = round(d['quantity'] / d['m_count'], 2) 
  return descs



def departments(request):

  if request.method == 'GET':
    dept_grp = request.GET.get('dept_grp', '')
    query = um_ecomm_dept_units_rept.objects.filter(dept_grp=dept_grp)
    response = list(query.values_list('dept_descr', 'deptid').distinct())
  
    print response


# gives back a queryset given a string of dept ids separated by - and ,
def handleDeptQuery(dept_str):
  query = um_ecomm_dept_units_rept.objects.none() #start with an empty query
  ids = dept_str.split(',')

  for i in ids:
    if '-' in i:
      begin = int(i.split('-')[0])
      end = int(i.split('-')[1])
      newQuery = um_ecomm_dept_units_rept.objects.filter(deptid__lte=end, deptid__gte=begin)
    else:
      newQuery = um_ecomm_dept_units_rept.objects.filter(deptid=int(i))

    query = query | newQuery #chain our queries but union them

  return query 
















