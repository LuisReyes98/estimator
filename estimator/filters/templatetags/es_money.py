from django.template import Library
from money import Money
import json


register = Library()


@register.filter(is_safe=True)
def es_money(obj):
    try:
        num = float(obj)
        m = Money(('%.2f' % num), 'VEF')

        return (m.format('es_ES', '#,##0.00'))
    except Exception as ex:
        print(ex)
        return (obj)
