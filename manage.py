#!/usr/bin/env python
import sys
import os

from os.path import abspath, dirname, join

try:
    import pinax
except ImportError:
    sys.stderr.write("Error: Can't import Pinax. Make sure you are in a "
        "virtual environment that has\nPinax installed.\n")
    sys.exit(1)
#else:
#    import pinax.env

from django.conf import settings
from django.core.management import setup_environ, execute_from_command_line

try:
    import denigma.settings as settings_mod # Assumed to be in the same directory.
except ImportError:
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


# setup the environment before we start accessing things in the settings.
setup_environ(settings_mod)
#pinax.env.setup_environ(__file__)

sys.path.insert(0, join(settings.PROJECT_ROOT, "apps"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "denigma.settings")
    execute_from_command_line()