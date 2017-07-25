from django import template

register = template.Library()

num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
           (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

def num2roman(num):

    # should be a number
@register.filter
def roman(value):
  num = int(value)

  # https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
  # probably overkill
  roman = ''
  while num > 0:
    for i, r in num_map:
      while num >= i:
        roman += r
        num -= i

  return num
