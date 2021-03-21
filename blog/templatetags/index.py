from django import template
register = template.Library()

@register.filter
def insta(indexable, i):
    return indexable[i].insta_handler 

@register.filter
def url(indexable, i):
    return indexable[i].url

@register.filter(name='times') 
def times(number):
    return range(number)

@register.filter(name='range') 
def filter_range(start, end):   
    return range(start, end+1)
