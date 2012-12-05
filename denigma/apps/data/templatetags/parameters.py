"""Provides templatetags to enable passing parameters to variables in templates.
"call" and "args" need to be used in joint conjunction and enable convenient
passing of arguments:

Arguments are set with "args" and the function is called with "call"::

    {{ entry|args:"200"|call:"brief" }}

Multiple arguments can be passed::

    {{ entry|args:arg1|args:arg2|call:"function" }}

The "method" templatetag enables to call a method with arguments as well as keyword arguments.
"""
from django import template

register = template.Library()


def call(obj, methodName):
    """Used in conjunction with args to call a method."""
    method = getattr(obj, methodName)

    if obj.__dict__.has_key("__callArg"):
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()

def args(obj, arg):
    """Used in conjunction with call to call a method."""
    if not obj.__dict__.has_key("__callArg"):
        obj.__callArg = []

    obj.__callArg += [arg]
    return obj

def method(obj, call):
    """Calls a method with its parameters (call) on an object (obj).
    {{ object|method:"name(parameters) }}"
    """
    return eval('obj.'+call)

register.filter("call", call)
register.filter("args", args)
register.filter("method", method)