
from django import template
from django.db import connection


register = template.Library()


@register.filter
def to_class_name(value):
    return value.__class__._meta.model.__name__


@register.filter
def db_provider(value):
    return connection.vendor
