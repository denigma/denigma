# -*- coding: utf8 -*-
"""Provides templatetags/filters to render mathematical expressions."""
import re
from django import template


register = template.Library()

@register.filter
def formula(value, uni=True):
    """Convertes all instance of decimal numbers of the form base*10^exp or baseE-exp in
    proper appearance for rendering."""
    if uni:
        multiplication = u'⋅'
    else:
        multiplication = '⋅'

    def translate(match):
        #return ":math:`%s`" % match.group(0)
        return "%s\ :sup:`%s`" % (match.group('base').replace('*', multiplication), match.group('exp')) #•.replace('*', '⋅')&#183;

    rc = re.compile('(?P<base>\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2})\^(?P<exp>-{0,1}\d+)')#'\d\**\d{1,2}\^-{0,1}\d+')
    value = rc.sub(translate, value)

    def transform(match):
        exp = match.group('exp')
        while exp.startswith('0'): #-
            exp = exp[1:] #
        return "%s*10\ :sup:`%s`".replace('*', multiplication) % (match.group('base'), '-'+exp) #

    rc = re.compile('(?P<base>\d+\.{0,1}\d+)[eE]-(?P<exp>-{0,1}\d+)')
    value = rc.sub(transform, value)

    return value.replace("CO2", "CO\ :sub:`2`")\
    .replace("H2O2", "H\ :sub:`2`O\ :sub:`1`")\
    .replace("H2O", "H\ :sub:`2`\ O")\
    .replace("Fe3+", "Fe\ :sub:`3+`")\
    .replace("Cu2+", "Cu\ :sub:`2+`")\
    .replace("NAD+", "NAD\ :sup:`+`")\
    #.replace("-/-", "\ :sup:`-/-`\ ")


if __name__ == '__main__':
    rc = re.compile('\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2}\^-{0,1}\d+')
    rc = re.compile('(?P<base>\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2})\^(?P<exp>-{0,1}\d+)')#'\d\**\d{1,2}\^-{0,1}\d+')
    rc = re.compile('(?P<base>\d+\.{0,1}\d+)[eE](?P<exp>-{0,1}\d*)')
    string = "Some text a number 2.5*10^-5"
    string = "lobin-like terms (< 2.7*10^-8) as we 2.5e-15"
    print re.findall(rc, string)
    print formula(string)