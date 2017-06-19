from django import forms

class MainForm(forms.Form):
  dept_id_range = forms.CharField(max_length=20)
  fiscal_yr = forms.ChoiceField(choices=((str(x), x) for x in range(2010,2018)))
