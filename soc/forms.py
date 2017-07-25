from django import forms
from models import um_ecomm_dept_units_rept, Search
from django.utils.dates import MONTHS

class MainForm(forms.Form):

  dept_id_range = forms.CharField(label='Department IDs', max_length=40, widget=forms.TextInput(attrs={'placeholder': 'type individual ids or a range of ids'}), required=False)

  DEPT_GRPS = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp', flat=True).distinct())

  DEPT_GRP_BUD_SEQ = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_bud_seq', flat=True).distinct())

  DEPT_GRP_VP  = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp_vp_area', flat=True).distinct())

  dept_grp_vp_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRP_VP))
  dept_grp_bud_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRP_BUD_SEQ))
  dept_grp_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRPS))

  fiscal_yr = forms.ChoiceField(required=False, choices=((str(x), x) for x in range(2017,2005, -1)))
  calendar_yr = forms.ChoiceField(required=False, choices=((str(x), x) for x in range(2017,2005, -1)))


  range_begin_m = forms.ChoiceField(choices=MONTHS.items())
  range_begin_y = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))
  
  range_end_m = forms.ChoiceField(choices=MONTHS.items())
  range_end_y = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))

  t_choice = forms.CharField(max_length=1)

  def save(self, dept, time):
    search = Search(dept=dept, time=time)
    search.save()

