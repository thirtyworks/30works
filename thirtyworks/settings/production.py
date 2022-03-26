from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config_json["DATABASE_NAME"],
        'USER': config_json["DATABASE_USERNAME"],
        'PASSWORD': config_json["DATABASE_PASSWORD"],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_json["SECRET_KEY"]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['thirty.works', 'www.thirty.works'] 


try:
    from .local import *
except ImportError:
    pass
