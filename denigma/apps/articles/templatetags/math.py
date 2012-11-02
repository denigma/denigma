#! -*- coding: utf8 -*-
import re
from django import template


register = template.Library()

@register.filter
def formula(value, uni=True):
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
        if exp.startswith('-0'):
            exp = '-'+exp[2:]
        return "%s*10\ :sup:`%s`".replace('*', multiplication) % (match.group('base'), exp) #

    rc = re.compile('(?P<base>\d+\.{0,1}\d+)[eE](?P<exp>-{0,1}\d+)')
    value = rc.sub(transform, value)

    return value.replace("CO2", "CO\ :sub:`2`")


if __name__ == '__main__':
    rc = re.compile('\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2}\^-{0,1}\d+')
    rc = re.compile('(?P<base>\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2})\^(?P<exp>-{0,1}\d+)')#'\d\**\d{1,2}\^-{0,1}\d+')
    rc = re.compile('(?P<base>\d+\.{0,1}\d+)[eE](?P<exp>-{0,1}\d*)')
    string = "Some text a number 2.5*10^-5"
    string = "lobin-like terms (< 2.7*10^-8) as we 2.5e-15"
    print re.findall(rc, string)
    print formula(string)