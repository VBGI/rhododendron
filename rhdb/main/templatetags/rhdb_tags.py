from django import template

register = template.Library()

@register.simple_tag
def render_map():
    '''Render current map'''

    return ''