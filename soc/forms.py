from django import forms
from models import um_ecomm_dept_units_rept, Search
from django.utils.dates import MONTHS

class MainForm(forms.Form):

  dept_id = forms.CharField(label='Department ID', max_length=20, required=False)

  dept_id_range = forms.CharField(label='Department IDs', widget=forms.Textarea(attrs={'placeholder': 'Separate individual departments with commas, and ranges with dashes (481054, 481060-481065)'}), required=False)

  DEPT_GRPS = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp', flat=True).distinct())

  DEPT_GRP_BUD_SEQ = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_bud_seq', flat=True).distinct())

  DEPT_GRP_VP  = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp_vp_area', flat=True).distinct())

  dept_grp_vp_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRP_VP))
  dept_grp_bud_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRP_BUD_SEQ))
  dept_grp_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRPS))

  fiscal_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))
  calendar_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))

  single_month_m = forms.ChoiceField(choices=MONTHS.items())
  single_month_y = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))


  range_begin_m = forms.ChoiceField(choices=MONTHS.items())
  range_begin_y = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))
  
  range_end_m = forms.ChoiceField(choices=MONTHS.items())
  range_end_y = forms.ChoiceField(choices=((str(x), x) for x in range(2017,2008, -1)))

  d_choice = forms.CharField(max_length=1)
  t_choice = forms.CharField(max_length=1)

  def clean(self):
    # logic for checking validness

  def save(self, dept, time):
    search = Search(dept=dept, time=time)
    search.save()

