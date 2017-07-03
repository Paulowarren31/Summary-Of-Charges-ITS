from django import template

register = template.Library()

@register.filter
def money(value):
  if value is not None and value != '':
    return "$" + "{:,.2f}".format(float(value))
  else:
    return ''

