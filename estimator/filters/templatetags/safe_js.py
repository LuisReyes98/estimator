from django.utils.safestring import mark_safe
from django.template import Library

import json


register = Library()


@register.filter(is_safe=True)
def safe_js(obj):
    try:
        return mark_safe(json.dumps(obj))
    except Exception as ex:
        print(ex)
        return mark_safe(json.dumps({}))
