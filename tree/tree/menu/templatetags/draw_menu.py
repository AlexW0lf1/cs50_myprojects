from django import template
from menu.models import Menu

register = template.Library

@register.inclusion_tag('menu/home.html', takes_context=True)
def draw_menu(slug, context):
    try:
        menu = Menu.objects.prefetch_related('items__items__items__items').get(slug=slug)
        return {'menu': menu, 'context': context}
    except Menu.DoesNotExist:
        return {'menu': '', 'context': context}
