# -*- coding: utf-8 -*-
import rst_directive
import youtube


VERSION = (1, 4, 1, "f") # Following PEP 386.
DEV_N = None


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version

__version__ = get_version()

__about__ = """
This project lays the foundation for deciphering life. It
provides the project directory layout and some key infrastructure apps on
which the other developments and enhancement of Denigma are based.
"""
