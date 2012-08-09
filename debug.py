#! /usr/bin/env python

debug_mode = """
BASE_URL="http://clktc.de"
DEBUG = True
TEMPLATE_DEBUG = True
SERVE_MEDIA = True

DATABASES = {
    "default": {
       "ENGINE": "mysql",
       "NAME": "clktc",
       "USER": "clktc",
       "PASSWORD": "48cebe53677c5b3",
       "HOST": "ec2-54-247-32-121.eu-west-1.compute.amazonaws.com",
    }
}

STATIC_URL = "/s"
STATIC_ROOT = "/home/clktc/clktc/media"
TEMPLATE_DIRS = ["/home/clktc/clktc/templates"]
"""

settings = open("/home/clktc/clktc/local_settings.py", 'w')
settings.write(debug_mode)
settings.close()


