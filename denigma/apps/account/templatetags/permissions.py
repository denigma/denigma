from django import template

register = template.Library()


@register.filter
def allowed(user, obj, type='view_entry'):
    return user.has_perm(type, obj)