from .base import *

DEBUG = False

DATABASES = {
    'default': {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config_json["DATABASE_NAME"],
        'USER': config_json["DATABASE_USERNAME"],
        'PASSWORD': config_json["DATABASE_PASSWORD"],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_json["SECRET_KEY"]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['thirty.works', 'www.thirty.works', '212.71.249.151'] 


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

try:
    from .local import *
except ImportError:
    pass
