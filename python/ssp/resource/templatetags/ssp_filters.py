#!coding:utf-8
from django import template
register = template.Library()

@register.filter(name='tpl_find')
def tpl_find(str, neddle):
    if str.find(neddle) >= 0:
        return True
    else:
        return False