from django import template
from django.utils import timezone
import jdatetime

register = template.Library()

@register.filter
def to_jalali(value):
    if value == "":
        return ""
    local_value = timezone.localtime(value)
    jalali_date = jdatetime.datetime.fromgregorian(datetime=local_value)
    return f"{jalali_date.hour:02d}:{jalali_date.minute:02d}  -  {jalali_date.year:04d}/{jalali_date.month:02d}/{jalali_date.day:02d}"