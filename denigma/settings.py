# -*- coding: utf-8 -*-
# Django settings for denigma project.

import os.path
import posixpath
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

BASE_URL="http://localhost:8000"

# tells Pinax to use the default theme
PINAX_THEME = "default"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

BACKEND = 'mysql' # Either sqlite3 or mysql as well as later on also postgres.

if BACKEND == 'sqlite3':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3", 	 # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
            "NAME": os.path.join(PROJECT_ROOT, "dev.db"),# Or path to database file if using sqlite3.
            "USER": "",                            	 # Not used with sqlite3.
            "PASSWORD": "",                         	 # Not used with sqlite3.
            "HOST": "",                             	 # Set to empty string for localhost. Not used with sqlite3.
            "PORT": "",                             	 # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "mysql",
            "NAME": 'denigma',
            "USER": "root",
            "PASWORD": "",
            "HOST": "",
            "PORT": "",
            "OPTIONS": {
                "init_command": "SET storage_engine = MYISAM",
            }
        }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/s/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "media"),
    os.path.join(PINAX_ROOT, "media", PINAX_THEME),
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = "$&li378l3_8wform1%!hphxb3_#bqomk!302kplo)16j1tp)z#"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
#    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",

#    #CMS:
#    "cms.middleware.multilingual.MultilingualURLMiddleware",
]    

ROOT_URLCONF = "denigma.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
]

##CMS:
#CMS_TEMPLATES = (
#    ('template_1.html', 'Template One'),
#    ('template_2.html', 'Template Two'),
#)
#LANGUAGES = [
# ('en', 'English'),
#]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static_url",
    
    "pinax.core.context_processors.pinax_settings",

#    #CMS:
#    "django.contrib.auth.context_processors.auth",
#    "cms.context_processors.media",
#    "sekizai.context_processors.sekizai",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.markup", 
   
    "pinax.templatetags",
    
    # external
    "staticfiles",
    "debug_toolbar",
    "south", # Intelligent schema and data migrations.
    "tagging",

#    "cms", # Content Management System.
#    "mptt", # Utilties for implementing a modified pre-order traversal tree.
#    "sekizai", # For javascipt and css management.
 
    # Pinax
    
    # project
    "shorty",
    "polls",
    "wiki",
    "southtut",
    "gallery",    
    "blogs",
    "links",
    "books",
    "todos",
]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass

# key.py can be used to introduce access and screte keys such as used for S3.
try:
    from key import *
except ImportError:
    pass
