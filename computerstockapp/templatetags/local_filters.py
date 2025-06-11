from django import template
from django.utils import timezone
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def local_datetime(value):
    """Convert UTC datetime to local timezone"""
    if value:
        return localtime(value)
    return value

@register.filter
def local_date_format(value, format_string="M d, Y g:i A"):
    """Format datetime in local timezone"""
    if value:
        local_dt = localtime(value)
        return local_dt.strftime(format_string)
    return ""
