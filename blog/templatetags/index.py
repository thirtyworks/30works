from django import template
from blog.views import get_event_day
import imghdr
import os

register = template.Library()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

@register.simple_tag
def get_num():   
    current_event_day = get_event_day()
    return [i for i in range(1, 31) if i <= current_event_day]

@register.simple_tag
def check_img_type(imgUrl):
    return imghdr.what(BASE_DIR + imgUrl)