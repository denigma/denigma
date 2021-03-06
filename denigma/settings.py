# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import posixpath
import pinax
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

BASE_URL= 'http://denigma.de' #'http://localhost:8000'

# tells Pinax to use the default theme
PINAX_THEME = 'basic'# "default"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

# django-compressor is turned off by default due to deployment overhead for
# most users. See <URL> for more information
COMPRESS = False

INTERNAL_IPS = [
    '127.0.0.1',
]

ADMINS = [
     ('Hevok', 'd.a.wuttke@gmail.com'), # 'Alerts', 'alerts@denigma.de'
]

CONTACT_EMAIL = 'hevok@denigma.de'
DEFAULT_FROM_EMAIL = 'hevok@denigma.de'
SERVER_EMAIL = 'd.a.wuttke@gmail.com' #'hevok@denigma.de'

MANAGERS = ADMINS

SEND_BROKEN_LINK_EMAILS = False # Report 404 errors too.

if os.path.exists(os.path.join(PROJECT_ROOT, 'local_settings.py')):
    BACKEND = 'mysql'
else:
    BACKEND = 'sqlite3'
# Either sqlite3 or mysql as well as later on also postgres.
if BACKEND == 'sqlite3': # Development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3', 	 # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
            'NAME': os.path.join(PROJECT_ROOT, 'dev.db'),# Or path to database file if using sqlite3.
            'USER': '',                            	 # Not used with sqlite3.
            'PASSWORD': '',                         	 # Not used with sqlite3.
            'HOST': '',                             	 # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                             	 # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'denigma',
            'USER': 'root',
            'PASWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {
                #'init_command': 'SET storage_engine = MYISAM',
                'init_command': 'SET storage_engine = INNODB,  \
                                 SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
            }
        }
    }

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'whoosh_index'),
    },
}

HAYSTACK_SEARCH_RESULTS_PER_PAGE = 25

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT,  'site_media/media') #'/site_media/',

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/media/'

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static') #'site_media', 'static')

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
#STATIC_URL = "/site_media/static/"
STATIC_URL = '/s/'

# Additional directories which hold static files
STATICFILES_DIRS = [
    #os.path.join(PROJECT_ROOT, "static"),
    os.path.join(PROJECT_ROOT, 'media'),
    os.path.join(PINAX_ROOT, 'media', PINAX_THEME),
    os.path.join(BASE_DIR, 'semantictasks')
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder', #    'staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder', #     'staticfiles.finders.AppDirectoriesFinder',
    #'staticfiles.finders.LegacyAppDirectoriesFinder',
    #'compressor.finders.CompressorFinder',
    'coffeescript.finders.CoffeescriptFinder',
    'less.finders.LessFinder',
)

COFFEESCRIPT_MTIME_DELAY = 1
#COFFEESCRIPT_ROOT = '/s/'
COFFEESCRIPT_OUTPUT_DIR =  "js" #os.path.join(PROJECT_ROOT,)


LESS_MTIME_DELAY = 1
#LESS_ROOT = '/s/'
LESS_OUTPUT_DIR =  "css" #os.path.join(PROJECT_ROOT,)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, 'admin/')

# Subdirectory of COMPRESS_ROOT to store the cached media files in
COMPRESS_OUTPUT_DIR = 'cache'

# Memcache
CACHES = {
    'default': {
        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
        'LOCATION': 'localhost:11211',
        'TIMEOUT': 500,
        'BINARY': True,
        'OPTIONS': { # Maps to pylibmc "behaviours"
            'tcp_nodelay': True,
            'ketama': True# }
            }
    }
}

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$&li378l3_8wform1%!hphxb3_#bqomk!302kplo)16j1tp)z#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [ # Redundant?
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.filesystem.load_template_source',       # Depricated in
    #'django.template.loaders.app_directories.load_template_source',  # Django-1.4.
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware', # For ...
    #'reversion.middleware.RevisionMiddleware',                     # reversions control.
    'django_openid.consumer.SessionConsumer',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pinax.apps.account.middleware.LocaleMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #'pinax.middleware.security.HideSensistiveFieldsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'track.middleware.VisitorTrackMiddleware',
    'track.middleware.BannedIPMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'honeypot.middleware.HoneypotMiddleware',
#    #CMS:
#    "cms.middleware.multilingual.MultilingualURLMiddleware',
]

ROOT_URLCONF = 'denigma.urls'

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(PINAX_ROOT, 'templates', PINAX_THEME),
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
    'django.contrib.auth.context_processors.auth', # Redundant?
    'django.core.context_processors.debug', # Redundant?
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',#
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    
    'staticfiles.context_processors.static', # Redundant?
    'staticfiles.context_processors.static_url', # Redundant?
    
    'pinax.core.context_processors.pinax_settings',
    
    'pinax.apps.account.context_processors.account',
    
    'notification.context_processors.notification',
    'announcements.context_processors.site_wide_announcements',

#    #CMS:
#    'django.contrib.auth.context_processors.auth',
#    'cms.context_processors.media',
#    'sekizai.context_processors.sekizai',
]

INSTALLED_APPS = [
    # Alternative admin designs:
    #'grappelli',
    #'djangocms_admin_style',
    #'django_admin_bootstrapped',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.flatpages',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.markup',

    'pinax.templatetags',
    
    # theme
    'pinax_theme_bootstrap',
    #'pinax_theme_bootstrap_account',
    #'django_forms_bootstrap',
    
    # external
    'notification', # must be first
    #'staticfiles',
    #'compressor',
    'debug_toolbar',
    'mailer',
    'django_openid',
    'timezones',
    'emailconfirmation',
    'announcements',
    'pagination',
    'idios', # UserProfiles
    'metron',
    'south',   # Intelligent schema and data migrations.
    'taggit',
    'tagging',
    'reversion',# Revision-control for models.
    'haystack', # Searching
    'django_tables2',
    'django_tablib',

    'django_filters',
    #'ajax_filtered_fields',
    'mptt', # Hierarchy: Utilties for implementing a modified pre-order traversal tree.
    'pagedown', # Markdown preview editor
    'google_analytics',

    'guardian', # Permissions

    'coffeescript',
    'less',

    # API Framworks:
    #'tastypie',
    'rest_framework',

    # Comments and forms:
    'fluent_comments',
    'crispy_forms',
    'django.contrib.comments',
    'honeypot',
    'templateaddons',
#    'cms", # Content Management System.
#    'sekizai", # For javascipt and css management.
    
    # Pinax
    'account',
    'pinax.apps.signup_codes',
    
    # project
    'home',
    'polls',
    'questionnaire',
    'donation',

    'data',
    'blogs',
    'blog',
    'wiki',
    'tutorials',
    'articles',
    #'news',

    'media',
    'links',
    'shorty',

    'duties',
    'tasks',
    'todos',
    #'todo',
    'quests',
    'task',
    #'files',

    # Communication
    'pastebin',
    'channel',
    'chat',
    'video',

    # Integrator
    'annotations',
    'interactions',
    'expressions',
    'datasets',
    'lifespan',

    'about',
    'aspects',
    'profiles',
    'avatar',  # django-avatar: Representative user images
    'track',

    'experts',
    'southtut',

    'books',
    'chrono',
    'meta',
    'eva',
    'alliance',
    'immuno',
    'ontology',
    'network',

    'stats',
    'utils',
    'add',
    #'triple',
    'longevitydb',
]

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, 'fixtures'),
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

EMAIL_BACKEND = 'mailer.backend.DbBackend'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: '/profiles/profile/%s/' % o.username,
}

AUTH_PROFILE_MODULE = 'profiles.Profile'
NOTIFICATION_LANGUAGE_MODULE = 'account.Account'

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_USE_OPENID = False
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

AUTHENTICATION_BACKENDS = [
    'pinax.apps.account.auth_backends.AuthenticationBackend',
    #'announcements.auth_backends.AnnouncementPermissionsBackend',
    'guardian.backends.ObjectPermissionBackend',
]

ANONYMOUS_USER_ID = -1

LOGIN_URL = '/account/login/' # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = 'what_next'
LOGOUT_REDIRECT_URLNAME = 'home'

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Chatting:
CHAT_HTTP_PORT = 8080
CHAT_HOST = None

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
    CHAT_HTTP_HOST = CHAT_HOST or DATABASES['default']['HOST']
except ImportError:
    pass

# key.py can be used to introduce access and screte keys such as used for S3.
try:
    from key import *
except ImportError:
    pass

# Load the alternative admin interface:
try:
    if 'GRAPPELLI' in globals() and GRAPPELLI:
        INSTALLED_APPS.insert(0, 'grappelli')
        GRAPPELLI_ADMIN_HEADLINE = 'Denigma'
        GRAPPELLI_ADMIN_TITLE = 'Denigma'
        ADMIN_MEDIA_PREFIX = STATIC_URL + 'grappelli/' # for grappelli 2.3.8 only.
except ImportError:
   pass

#BANISH_ENABLED = True

DONATION_NAME = 'Denigma'
DONATION_NUMBER = 'The Digital Decipher Machine'
PAYPAL_ID = 'daniel.wuttke@gmx.de'

GOOGLE_ANALYTICS_MODEL = True

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',

    ],
    'PAGINATE_BY': 10,
}
# Honeypot:
HONEYPOT_FIELD_NAME = 'phonenumber'

CRISPY_TEMPLATE_PACK = 'bootstrap'