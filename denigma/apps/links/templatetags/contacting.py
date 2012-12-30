from django.template import Library


register = Library()

@register.filter
def contact(value):
    if value:
        if "@" in value:
            return '<a href="mailto:%s">%s</a>' % (value, value.replace('@', '(at)'))
        elif value.startswith('http'):
            return '<a href="%s">%s</a>' % (value, value.replace('www.', '').split('://')[-1])
        elif value.startswith('www.'):
            return '<a href="http://%s">%s</a>' % (value, value.split('www.')[-1])
        else:
            return value
    else:
        return value