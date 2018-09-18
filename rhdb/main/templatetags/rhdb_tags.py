from django import template

register = template.Library()
import re

inline_album_pat = r'\{\{\s?(\w+)\s?\}\}'

@register.simple_tag
def render_map():
    '''Render current map'''

    return ''


@register.filter
def render_albums(value, arg):

    return value.replace(arg, '')