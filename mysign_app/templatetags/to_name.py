from django import template

register = template.Library()


@register.filter
def to_name(value):
    """ Replace all dots and underscores with space"""
    return value.replace(".", " ").replace('_', ' ')
