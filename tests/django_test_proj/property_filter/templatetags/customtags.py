
from django import template

register = template.Library()
@register.filter
def to_class_name(value):
    return value.__class__._meta.model.__name__
