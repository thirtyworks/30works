from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u1oa84ms#sf4hyrex=o%1om$gv@u1o$j$+0$h4pu0vrw#ii_-v'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

try:
    from .local import *
except ImportError:
    pass
