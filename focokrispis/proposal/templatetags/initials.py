from django import template

register = template.Library()

@register.filter
def initials(value):
    return value[0:1]