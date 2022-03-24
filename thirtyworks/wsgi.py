"""
WSGI config for thirtyworks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config_file = os.path.join(BASE_DIR, '30works.json')
with open(config_file, 'r') as f:
    config_json = json.load(f)

# add the thirtyworks project path into the sys.path
sys.path.append('/home/ubuntu/thirty-works/thirtyworks')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/home/ubuntu/virtualenvs/30env/lib/python3.6/site-packages')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config_json["DJANGO_SETTINGS_MODULE"])

application = get_wsgi_application()