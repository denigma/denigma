from django import template
from django.conf import settings as django_settings
from django.db.models import Min, Max

from denigma.apps.chat.models import Message
from denigma.apps.chat.conf import settings


register = template.Library()


@register.inclusion_tag('chat/nav.html', takes_context=True)
def chat_nav(context):
    min_max = Message.objects.aggregate(Min('time'),
                                        Max('time'))
    if min_max.values()[0]:
        years = range(min_max['time__max'].year,
                      min_max['time__min'].year - 1, -1)
    else:
        years = []
    context['IRC_CHANNEL'] = settings.IRC_CHANNEL
    context['years'] = years
    context['LOGOUT_URL'] =django_settings.LOGOUT_URL
    return context