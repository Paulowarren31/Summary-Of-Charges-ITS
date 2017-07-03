from django import template
import locale

register = template.Library()

locale.setlocale(locale.LC_ALL, '')

@register.filter
def money(value):
  print type(value)
  if type(value) == unicode:
    print value
    print value != ''
    print value is ''
  if value is not None and value != '':
    return locale.currency(float(value), grouping=True)
  else:
    return ''

