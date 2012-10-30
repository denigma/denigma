#! -*- coding: utf8 -*-
import re
from django import template


register = template.Library()

@register.filter
def formula(value):
    rc = re.compile('(?P<base>\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2})\^(?P<exp>-{0,1}\d+)')#'\d\**\d{1,2}\^-{0,1}\d+')
        #return ":math:`%s`" % match.group(0)
        return "%s\ :sup:`%s`" % (match.group('base').replace('*', u'⋅'), match.group('exp')) #•.replace('*', '⋅')&#183;
    result = rc.sub(translate, value)
    return result

if __name__ == '__main__':
    rc = re.compile('\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2}\^-{0,1}\d+')
    rc = re.compile('(?P<base>\d{0,1}\.{0,1}\d*\*{0,1}\d{1,2})\^(?P<exp>-{0,1}\d+)')#'\d\**\d{1,2}\^-{0,1}\d+')
    string = "Some text a number 2.5*10^-5"
    string = "lobin-like terms (< 10^-8) as we"
    print re.findall(rc, string)