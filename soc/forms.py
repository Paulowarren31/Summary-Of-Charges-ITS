from django import forms
from models import um_ecomm_dept_units_rept, Search

class MainForm(forms.Form):
  dept_id = forms.CharField(label='Department ID', max_length=20, required=False)
  dept_id_range = forms.CharField(label='Department IDs', help_text='Separate individual departments with commas, and ranges with dashes (481054, 481060-481065)', widget=forms.Textarea, required=False)

  DEPT_GRPS = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp', flat=True).distinct())

  DEPT_GRP_BUD_SEQ = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_bud_seq', flat=True).distinct())

  DEPT_GRP_VP  = list(um_ecomm_dept_units_rept.objects.order_by().values_list('dept_grp_vp_area', flat=True).distinct())

  dept_grp_vp_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRP_VP))
  dept_grp_bud_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRP_BUD_SEQ))
  dept_grp_choice = forms.ChoiceField(required=False, choices=((x, x.replace('_', ' ').lower()) for x in DEPT_GRPS))

  fiscal_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2018,2008, -1)))

  calendar_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2018,2008, -1)))
  single_month = forms.DateField(required=False)


  def save(self, dept, time):
    save = Search.objects.create(dept=dept, time=time)
    save.save()

  def clean(self):
    cleaned_data = super(MainForm, self).clean()

    dept_id = cleaned_data.get('dept_id')
    dept_id_range = cleaned_data.get('dept_id_range')

    if dept_id and dept_id_range:
      raise forms.ValidationError("You may only use one type of dept select")


    # if something:

