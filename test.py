import django

django.setup()

from soc.models import um_ecomm_dept_units_rept
from django.shortcuts import render
from django.test.client import RequestFactory

res = {}

query = um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp_vp_area','dept_grp_vp_area_descr').distinct()

vp_groups =list(query)

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

print final_groups
    

res['d'] = final_groups


request = RequestFactory().get('/')

content = render(request, 'index.html', res) 

with open('test.html', 'w') as s_file:
  s_file.write(str(content))
  print 'saved PogChamp'



