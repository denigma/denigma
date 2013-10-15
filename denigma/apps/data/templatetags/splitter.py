from django import template

register = template.Library()


@register.filter()
def snap(text):
    splitter = text.split('\n')
    if len(splitter) == 1:
        return text
    return "\n".join(splitter[:-1])

@register.filter(name='split')
def split(value, arg):
    return value.split(' ')[1]