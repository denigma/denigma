import logging
import traceback
from datetime import datetime, timedelta

from django.db import models

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from manager import VisitorManager

log = logging.getLogger(__file__)


class Visitor(models.Model):
    session_key = models.CharField(max_length=40) # primary_key=True?
    ip_address = models.CharField(max_length=39)
    user = models.ForeignKey(User, null=True, related_name='visit_history')
    user_agent = models.CharField(max_length=255) #TextField()?

    referrer = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    page_views = models.PositiveIntegerField(default=0)
    session_start = models.DateTimeField()
    last_update = models.DateTimeField()

    start_time = models.DateTimeField(default=datetime.now())
    expiry_age = models.IntegerField(null=True)
    expiry_time = models.DateTimeField(null=True)
    time_on_site = models.IntegerField(null=True)
    end_time = models.DateTimeField(null=True)

    objects = VisitorManager()

    def _time_on_site(self):
        """Attempts to determine the amount of time a visitor has spent on the
        site based upon their information that's in the database."""
        if self.session_start:
            seconds = (self.last_update - self.session_start).seconds

            hours = seconds / 3600
            seconds -= hours * 3600
            minutes = seconds / 60
            seconds -= minutes * 60

            return u'%i:%02i;%02i' % (hours, minutes, seconds)
        else:
            return ugettext(u'unknown')
    time_on_site = property(_time_on_site)

    def session_expired(self):
        """The session has ended due to session expiration."""
        if self.expiry_time:
            return self.expiry_time <= datetime.now()
        return False
    session_expired.boolean = True

    def session_ended(self):
        """The session has ended due to an explicit logout."""
        return bool(self.end_time)
    session_ended.boolean = True

    def __unicode__(self):
        return u"%s %s %s" % (self.ip_address, self.url, self.page_views)


class Activity(models.Model):
    visitor = models.ForeignKey(Visitor, related_name='activity')
    url = models.CharField(max_length=255)
    view_time = models.DateTimeField()

    class Meta(object):
        ordering = ('-view_time',)


class UntrackedUserAgent(models.Model):
    keyword = models.CharField(_('keyword'), max_length=100,
        help_text='Part or all of a user-agent string.')

    def __unicode__(self):
        return self.keyword

    class Meta:
        ordering = ('keyword',)
        verbose_name = _('Untracked User-Agent')
        verbose_name_plural = _('Untracked User-Agents')


class BannedIP(models.Model):
    ip_address = models.IPAddressField('IP Address',
        help_text=_('The IP address that be banned'))

    def __unicode__(self):
        return self.ip_address

    class Meta:
        ordering = ('ip_address',)
        verbose_name = _('Banned IP')
        verbose_name_plural = _('Banned IPs')