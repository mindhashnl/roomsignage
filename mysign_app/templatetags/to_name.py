from django import template

register = template.Library()


@register.filter
def to_name(value):
    """
    Replace all underscores with space, and only take first path when with relationship
    So first_name becomes first name
    And company.name becomes company
    """
    return value.split('.')[0].replace('_', ' ')
