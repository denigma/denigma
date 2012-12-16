from datetime import datetime
import traceback
import logging

from django.conf import settings
from django.http import Http404, HttpResponse
from django.template import Context, loader
from django.utils.simplejson import JSONEncoder
from django.utils.translation import ungettext
from django.views.decorators.cache import never_cache

from models import Visitor
from utils import u_clean as uc

DEFAULT_TRACK_TEMPLATE = getattr(settings, 'DEFAULT_TRACK_TEMPLATE',
                                           'track/visitor_map.html')
log = logging.getLogger('track.views')


def update_active_users(request):
    """Returns a list of all active users."""
    if request.is_ajax():
        active = Visitor.objects.active()
        user = getattr(request, 'user', None)

        info = {
            'active': active,
            'registered': active.filter(user__isnull=False),
            'guests': active.filter(user__isnull=True),
            'user': user
        }

        # Render the list of active users
        t = loader.get_template('track/_active_users.html')
        c = Context(info)
        users = {'users': t.render(c)}

        return HttpResponse(content=JSONEncoder().encode(users))

    # If the request was not made via AJAX, raise a 404
    raise Http404

@never_cache
def get_active_users(request):
    """Retrieves a list of active users which is returned as plain JSON for
    easier manipulation with JavaScript."""
    if request.is_ajax():
        active = Visitor.objects.active().reverse()
        now = datetime.now()

        # We don't put the session key or IP address here for security reasons
        try:
            data = {'users': [{
                    'id': v.id,
                    #'user': uc(v.user),
                    'user_agent': uc(v.user_agent),
                    'referrer': uc(v.referrer),
                    'url': uc(v.url),
                    'page_views': v.page_views,
                    'geoip': v.geoip_data_json,
                    'last_update': (now - v.last_update).seconds,
                    'friendly_time': ', '.join(friendly_time((now - v.last_update).seconds)),
            } for v in active]}

        except:
            log.error('There was a problem putting all of the visitors data together:\n%s\n\n%s' % (traceback.format_exc(), locals()))
            return HttpResponse(content='{}', mimetype='text/javascript')

        response = HttpResponse(content=JSONEncoder().encode(data),
                                mimetype='text/javascript')
        response['Content-Length'] = len(response.content)

        return response

    # if the request was not made via AJAX, raise a 404
    raise Http404

def friendly_time(last_update):
    minutes = last_update / 60
    seconds = last_update % 60

    friendly_time = []
    if minutes > 0:
        friendly_time.append(ungettext(
            '%(minutes)i minute',
            '%(minutes)i minutes',
            minutes
        ) % {'minutes': minutes})
    if seconds > 0:
        friendly_time.append(ungettext(
            '%(seconds)i second',
            '%(seconds)i seconds',
            seconds
        ) % {'seconds': seconds})

    return friendly_time or 0

