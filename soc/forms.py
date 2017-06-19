from django import forms

class MainForm(forms.Form):
  dept_id = forms.CharField(max_length=20, required=False)
  dept_id_range = forms.CharField(max_length=20, required=False)
  fiscal_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2010,2018)))
