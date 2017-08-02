import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import MainForm
from decorators import user_has_permission
from models import um_ecomm_dept_units_rept
from django.db import models
from django.http import JsonResponse, Http404
import re
import xlsxwriter

from . import database
from django.conf import settings

import requests
import base64

#TODO
# month queries are buggy

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

    return JsonResponse({'list': dept_list})

# table view
@login_required(login_url='/accounts/login')
@user_has_permission
def table(request):

  form = MainForm()
  # if coming from index
  if request.method == 'POST':
    request.session['post'] = request.POST
    accounts, total, unit, date_range = handlePost(request.POST)


    if accounts == 'error':
      return render(request, 'index.html', {'form': form})

    return render(request, 'table.html', {'accounts': accounts, 'total': total, 'unit': unit, 'dateRange': date_range})

  else: #if not POST request
    return render(request, 'index.html', {'form': form})

def handlePost(post):

  form = MainForm(post)
  if form.is_valid():
    print 'clean form'

    cd = form.cleaned_data
    date_range = ''
    unit = ''

    choice2 = int(cd.get('t_choice'))

    print choice2

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

    elif choice2 == 3:
      b_month = cd.get('range_begin_m')

      if len(b_month) == 1:
        b_month = b_month.zfill(2)

      b_year = cd.get('range_begin_y')

      e_month = cd.get('range_end_m')

      if len(e_month) == 1:
        e_month = e_month.zfill(2)

      e_year = cd.get('range_end_y')

      date_range = b_month + '/' + b_year + ' to ' + e_month + '/' + e_year

      b_query = query.filter(calendar_yr__gte=b_year, month__gte=b_month)
      print list(b_query)
      e_query = query.filter(calendar_yr__lte=e_year, month__lte=e_month)
      print list(e_query)
      query = (b_query & e_query).distinct()
      print list(query)

    rows = list(query)

    print rows

    accounts, total = handleAccounts(rows)

    for acc in accounts:
      acc['items'] = handleGroups(acc)
      for group in acc['items']:
        group['items'] = handleDescriptions(group)

    form.save(unit, date_range) # save what they searched for

    print accounts
    

    return accounts, total, unit, date_range # returns tuple of all of the info we need to display

  else: #if form has errors
    print form.errors
    return 'error', form, False, False

# tries to convert a string to a float, returns 0 if exception, used for display
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
    elif '.' in i:
      scope = i.split('.')[0]
      val = i.split('.')[1]
      if scope == 'd':
        newQuery = um_ecomm_dept_units_rept.objects.filter(deptid=int(val))
      elif scope == 'g':
        newQuery = um_ecomm_dept_units_rept.objects.filter(dept_grp=val)
      elif scope == 'v':
        newQuery = um_ecomm_dept_units_rept.objects.filter(dept_grp_vp_area=val)
    else:
      newQuery = um_ecomm_dept_units_rept.objects.filter(deptid=int(i))

    query = query | newQuery #chain our queries but union them

  return query 

def hasNumbers(string):
  return bool(re.search(r'\d', string))


def download(request):
  post = request.session.get('post')
  accounts, total, unit, date_range = handlePost(post)


  wb = xlsxwriter.Workbook('sheet.xlsx')
  ws = wb.add_worksheet()


  header = wb.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
  money = wb.add_format({'num_format': '$#.#0'})
  bold = wb.add_format({'bold': True})


  ws.set_column(0, 1, 25)
  ws.set_column(2, 2, 15)
  ws.set_column(3, 5, 10)
  ws.set_column(6, 8, 15)

  ws.write(3, 0, 'Expense\nAccount', header)
  ws.write(3, 1, 'Item\nDescription', header)
  ws.write(3, 2, 'Charge\nCodes', header)
  ws.write(3, 3, 'Rate', header)
  ws.write(3, 4, 'Average Monthly Units Billed', header)
  ws.write(3, 5, 'Billed\nUnits', header)
  ws.write(3, 6, 'Item\nTotal', header)
  ws.write(3, 7, 'Item\nGroup Total', header)
  ws.write(3, 8, 'Account\nTotal', header)


  row = 3
  for item in accounts:
    row = row + 1
    ws.write(row, 8, item['total'], money)
    ws.write(row, 0, item['desc'] + " (" + item['num'] + ")", bold)
    for sub in item['items']:
      row = row + 1
      ws.write(row, 7, sub['total'], money)
      ws.write(row, 0, sub['grp'])
      row = row + 1
      for i in sub['items']:
        ws.write(row, 1, i['descr'])
        ws.write(row, 2, i['cc'])
        ws.write(row, 3, i['monthly'], money)
        ws.write(row, 4, i['unit_rate'])
        ws.write(row, 5, i['quantity'])
        ws.write(row, 6, i['total'], money)
        row = row + 1
    

  wb.close()

  fsock = open('/code/sheet.xlsx', "rb")

  response = HttpResponse(fsock, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  response['Content-Disposition'] = 'attachment; filename=' + unit + ' ' + date_range + 'report.xlsx'

  os.remove('/code/sheet.xlsx')

  return response


def search(request):
  if request.method == 'GET':
    search = request.GET.get('search', '')

    query = um_ecomm_dept_units_rept.objects.filter(dept_grp_vp_area__icontains=search).order_by().values_list('dept_grp_vp_area','dept_grp_vp_area_descr').distinct()
    vp_groups = list(query)

    final_groups = []

    # each vp is a tuple of 2 
    for vp in vp_groups:

      #get all dept_grps from each vp_group
      query = um_ecomm_dept_units_rept.objects.filter(dept_grp_vp_area=vp[0]).order_by().values_list('dept_grp','dept_grp_descr').distinct()

      vp = list(vp)
      vp.append(list(query)) # vp[2] is now the list of dept_grps associated with that thing

      # each dept_grp is a tuple of 2
      idx = 0
      for dept_grp in vp[2]:
        query = um_ecomm_dept_units_rept.objects.filter(dept_grp=dept_grp[0]).order_by().values_list('deptid','dept_descr').distinct()

        vp[2][idx] = list(vp[2][idx])
        vp[2][idx].append(list(query))
        idx += 1

      final_groups.append(vp)
        


    #vps = list(query)

    #tree = []
    #
    #for vp in vps:
    #  query = um_ecomm_dept_units_rept.objects.filter(dept_grp=vp[0]).order_by().values_list('dept_grp','dept_grp_descr').distinct()
    #  vp = list(vp)
    #  vp.append(list(query)) # vp[2] is now the list of dept_grps associated with that thing

    #  idx = 0
    #  for group in vp[2]:
    #    query = um_ecomm_dept_units_rept.objects.filter(dept_grp=group[0]).order_by().values_list('deptid','dept_descr').distinct()

    #    vp[2][idx] = list(vp[2][idx])
    #    vp[2][idx].append(list(query))
    #    idx += 1
    #    print vp

    #  tree.append(vp)

    #print tree

    return render(request, 'tree-dynamic.html', {'d': final_groups})

    #get all unique bud seqs that match search,
    # for each bud seq, get all unique vp grps 
      # for each vp grp, get all 

def list_append(lst, item):
  lst.append(item)
  return item












