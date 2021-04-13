from django import template

register = template.Library()

@register.assignment_tag
def split(str,splitter,index):
    return (str.split(splitter))[index]