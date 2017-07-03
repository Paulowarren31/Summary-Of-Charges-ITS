from django import forms
from models import um_ecomm_dept_units_rept

class MainForm(forms.Form):
  dept_id = forms.CharField(max_length=20, required=False)
  dept_id_range = forms.CharField(max_length=20, required=False)
  fiscal_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2018,2008, -1)))

  def clean(self):
    cleaned_data = super(MainForm, self).clean()

    dept_id = cleaned_data.get('dept_id')
    dept_id_range = cleaned_data.get('dept_id_range')

    if dept_id and dept_id_range:
      raise forms.ValidationError("You may only use one type of dept select")


    # if something:

