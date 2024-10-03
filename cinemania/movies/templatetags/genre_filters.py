from django import template



register = template.Library()

@register.filter
def get_item(genre_dict, key):
    return genre_dict.get(key, '')