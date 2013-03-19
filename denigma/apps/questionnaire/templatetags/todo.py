from django import template
from django.conf import settings

register = template.Library()


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

def get(value, arg):
    return value[arg]

def concat(value, arg):
    return value + arg


letters = map(chr, range(65, 91))
mapping = dict(zip(range(1, len(letters)), letters))

def number_letter(value, start=1):
    if '::' in value:
        value = value.split('::')[1]
    return mapping[int(value.split('-')[0])+int(start)-1]

def get_footnotes(questionnaire, section):
    return questionnaire.section_footnotes[section]

register.filter("getattribute", getattribute)
register.filter("get", get)
register.filter("concat", concat)

register.filter("number_letter", number_letter)
register.filter("get_footnotes", get_footnotes)