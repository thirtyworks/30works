from django import template
from datetime import datetime
from blog.views import get_event_day
import json
import imghdr
import os

register = template.Library()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Gets private data from '30works.json' file. FILE MOST BE IN ROOT DIRECTORY.
with open(os.path.join(BASE_DIR, '30works.json'), 'r') as f:
    config_json = json.load(f)

@register.filter
def insta(indexable, i):
    return indexable[i].insta_handler 

@register.filter
def url(indexable, i):
    return indexable[i].url

@register.simple_tag
def get_event_days():   
    """
    Return list days (numbers) from the past event days to current day
    """
    current_event_day = get_event_day()
    return [i for i in range(1, 31) if i <= current_event_day]

@register.simple_tag
def is_event_ready(now, release_date):   
    """
    Return True or False based on if the event started
    """
    current_date = datetime.strptime(now, "%d-%m-%Y, %X")
    is_event_ready = True if current_date > release_date else False
    return is_event_ready

@register.simple_tag
def get_event_release_date():   
    """
    Return the date the event starts
    """
    release_date = datetime.strptime(config_json.get('RELEASE_DATE', '01-04-2022'), "%d-%m-%Y, %X") 
    return release_date

@register.simple_tag
def check_img_type(imgUrl):
    """
    Return the type of an image (GIF, JPG, PNG).
    """
    return imghdr.what(BASE_DIR + imgUrl)