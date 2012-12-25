import re
import logging
import traceback
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.utils import DatabaseError
from django.http import Http404

import utils
from settings import TRACK_ACTIVITIES, TRACK_IGNORE_URLS
from models import Visitor, UntrackedUserAgent, BannedIP, Activity

TRACK_IGNORE_URLS = map(lambda x: re.compile(x), TRACK_IGNORE_URLS)

title_re = re.compile('<title?(.*?)</title>')
log = logging.getLogger('track.middleware')

class VisitorTrackMiddleware(object):
    """Keeps track of your active users."""

    @property
    def prefixes(self):
        """Returns a list of URL prefixes that we should not track."""
        if not hasattr(self, '_prefixes'):
            self._prefixes = getattr(settings, 'NO_TRACKING_PREFIXES', [])

            if not getattr(settings, '_FREEZE_TRACKING_PREFIXES', False):
                for name in ('MEDIA_URL', 'STATIC_URL'):
                    url = getattr(settings, name)
                    if url and url != '/':
                        self._prefixes.append(url)
                try:
                    # Finally, don't track requests to the tracker update pages
                    self._prefixes.append(reverse('track-refresh-active-users'))
                except NoReverseMatch:
                    # django-track hasn't been included in the URLconf if we
                    # get here, which is not a bad thing.
                    pass

                settings.NO_TRACKING_PREFIXES = self._prefixes
                settings._FREEZE_TRACKING_PREFIXES = True

        return self._prefixes

    def process_request(self, request):
        # Don't process AJAX request
        if request.is_ajax(): return

        # Create some useful variables:
        ip_address = utils.get_ip(request)
        user_agent = unicode(request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')

        # Retrieve untracked user agents from cache
        ua_key = '_tracking_untracked_uas'
        untracked = cache.get(ua_key)
        if untracked is None:
            log.info("Updating untracked user agent cache")
            untracked = UntrackedUserAgent.objects.all()
            cache.set(ua_key, untracked, 3600)

        # See if the user agent is not supposed to be tracked.
        ACTIVITY = True
        for ua in untracked:
            # if the keyword is found in the user agent, stop tracking
            if user_agent.find(ua.keyword) != -1:
                if not ua.activity:
                    log.debug('Not tracking UA "%s" because of keyword: %s' % (user_agent, ua.keyword))
                    return
                else:
                    ACTIVITY = False

        if hasattr(request, 'session') and request.session.session_key:
            # Use the current session key if we can
            session_key = request.session.session_key
        else:
            # Otherwise just fake a session key
            session_key = '%s:%s' % (ip_address, user_agent)
            session_key = session_key[:40]

        # Ensure that the request.path does not begin with any of the prefixes
        for prefix in self.prefixes:
            if request.path.startswith(prefix):
                log.debug('Not tracking request to: %s' % request.path)
                return

        # If we get here, the URL needs to be tracked
        # determine what time it is
        now = datetime.now()

        attrs = {
            'session_key': session_key,
            'ip_address': ip_address
        }

        # For some reason, Vistors.objects.get_or_create is not working here
        try:
            visitor = Visitor.objects.get(**attrs)
        except Visitor.DoesNotExist:
            # See if there's a visitor with the same IP and user agent
            # within the last 5 minutes
            cutoff = now - timedelta(minutes=5)
            visitors = Visitor.objects.filter(
                ip_address=ip_address,
                user_agent=user_agent,
                last_update__gte=cutoff
            )

            if len(visitors):
                visitor = visitors[0]
                visitor.session_key = session_key
                log.debug('Using existing visitor for IP %s / UA %s: %s' % (ip_address, user_agent, visitor.id))
            else:
                # It's probably safe to assume that the visitor is brand new
                visitor = Visitor(**attrs)
                log.debug('Created a new visitor: %s' % attrs)

        except:
            return

        # Determine whether or not the user is logged in
        user = request.user
        if isinstance(user, AnonymousUser):
            user = None

        # Update the tracking information:
        visitor.user = user
        visitor.user_agent = user_agent

        # If the visitor record is new, or the visitor hasn't been here for
        # at least an hour, update their referrer URL.
        one_hour_ago = now - timedelta(hours=1)
        if not visitor.last_update or visitor.last_update <= one_hour_ago:
            visitor.referrer = utils.u_clean(request.META.get('HTTP_REFERER', 'unknown')[:255])

            # Reset the number of pages they've been to
            visitor.page_views = 0
            visitor.session_start = now

        visitor.url = request.path

        visitor.last_update = now


        # Tracking
        #time_on_site = 0
        #if visitor.start_time:
        #    time_on_site = (now - visitor.start_time).seconds
        #print("time_on_site %s (%s)" % (time_on_site, visitor.time_on_site))
        #visitor.time_on_site = time_on_site

        SAVE_ACTIVITY = False
        if TRACK_ACTIVITIES and ACTIVITY:
            # Match against `path_info` to not include the SCRIPT_NAME
            path = request.path_info.lstrip('/')
            for url in TRACK_IGNORE_URLS:
                if url.match(path):
                    break
            else:
                SAVE_ACTIVITY = True

                visitor.page_views += 1
        else:
            path = request.path_info.lstrip('/')
            for url in TRACK_IGNORE_URLS:
                if url.match(path):
                    break
            else:
                visitor.page_views += 1

        try:
            visitor.save()
        except DatabaseError:
            log.error('There was a problem saving visitor information:\n%s\n\n%s' % (traceback.format_exc(), locals()))

        if SAVE_ACTIVITY:
            activity = Activity(visitor=visitor, url=request.path, view_time=now)
            activity.save()


class VisitorCleanUpMiddleware:
    """Clean up old visitor tracking records in the database."""

    def process_request(self, request):
        timeout = utils.get_cleanup_timeout()

        if str(timeout).isdigit():
            log.debug('Cleaning up visitors older than %s hours' % timeout)
            timeout = datetime.now() - timedelta(hours=int(timeout))
            Visitor.objects.filter(last_update__lte=timeout).delete()


class BannedIPMiddleware:
    """Raises an Http404 error for any page request form a banned IP."""

    def process_request(self, request):
        key = '_tracking_banned_ips'
        ips = cache.get(key)
        if ips is None:
            # Compile a list of all banned IP addresses
            log.info('Updating banned IPs cache')
            ips = [b.ip_address for b in BannedIP.objects.all()]
            cache.set(key, ips, 3600)

        # Check to see if the current user's IP address is in that list
        if utils.get_ip(request) in ips:
            raise Http404