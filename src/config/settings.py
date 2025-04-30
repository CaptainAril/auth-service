from src.env import app

from .apps import INSTALLED_APPS as INSTALLED_APPS
from .cors import CORS_ALLOWED_ORIGINS as CORS_ALLOWED_ORIGINS
from .caches import CACHES as CACHES
from .logger import LOGGING as LOGGING
from .databases import DATABASES as DATABASES
from .databases import DATABASE_ROUTERS as DATABASE_ROUTERS
from .templates import TEMPLATES as TEMPLATES
from .middleware import MIDDLEWARE as MIDDLEWARE

SECRET_KEY = app["secret_key"]
DEBUG = app["debug"]
ALLOWED_HOSTS = app["allowed_hosts"]

ROOT_URLCONF = "src.config.urls"
ASGI_APPLICATION = "src.config.asgi.application"


STATIC_URL = "static/"
MEDIA_URL = "media/"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True
