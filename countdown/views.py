from django.shortcuts import render
from datetime import datetime
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Gets private data from '30works.json' file. FILE MOST BE IN ROOT DIRECTORY.
with open(os.path.join(BASE_DIR, '30works.json'), 'r') as f:
    config_json = json.load(f)


def countdown(request):
    release_date = datetime.strptime(config_json.get('RELEASE_DATE', '01-04-2022'), "%d-%m-%Y") 
    return render(request, "countdown.html", context={'release_date': release_date})
