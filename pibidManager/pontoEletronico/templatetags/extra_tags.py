__author__ = 'stepgalvao'

from django import template
from datetime import timedelta

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name = None):
    if (group_name==None):
        return user.groups.exists()
    return True if group_name in user.groups.values_list('name',flat=True) else False

@register.filter(name='group_name')
def group_name(user):
    if (user.groups.exists()):
        return user.groups.values_list('name',flat=True)[0]
    return "Sem grupo"

@register.filter(name='timedelta')
def time_deta(time_delta):
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours.__str__()+"h:"+minutes.__str__()+"m"
