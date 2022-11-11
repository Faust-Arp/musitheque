from django import template
import math

register = template.Library()


# Filtre utilisé pour faire une boucle "while" avec un for
@register.filter(name='time')
def time(number):
    int_number = int(number)
    return range(int_number)


# filtre pour récupérer le dernier chiffre d'un nombre
@register.filter(name='last')
def last(number):
    str_number = str(number)
    last_digit = str_number[-1]
    return last_digit


# Filtre utiliser pour arrondir au nombre entier supérieur
@register.filter(name='minus')
def minus(number):
    round_number = 5 - math.ceil(number)
    return round_number
