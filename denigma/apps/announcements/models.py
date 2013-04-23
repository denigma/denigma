from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
try:
    set
except NameError:
    from sets import Set as set # Python 2.3 fallback
from datetime import datetime

class AnnouncementManager(models.Manager):
    """A basic manager for dealing with announcements."""
    def current(self, exclude=[], site_wide=False, for_members=False):
        """Fetches and returns a queryset with the current announcements.
        This method takes the following parameters:

        ``exclude``
            A list of IDs that should be excluded from the queryset.

        ``site_wide``
            A boolean flag to filter to just site wide announcements.

        ``for_members``
            A boolean flag to allow member only announcements to be returned
            in addition to any others."""
        queryset = self.all()
        if site_wide:
            queryset = queryset.filter(site_wide=True)
        if exclude:
            queryset = queryset.exclude(pk__in=exclude)
        if not for_members:
            queryset = queryset.filter(members_only=False)
        queryset = queryset.filter(Q(publish_end__gte=datetime.now()) | Q(publish_end=None)).order_by("-creation_date")
        return queryset


class Announcement(models.Model):
    """A single announcement."""
    DISMISSAL_NO = 1
    DISMISSAL_SESSION = 2
    DISMISSAL_PERMANENT = 3

    DISMISSAL_CHOICES = [
        (DISMISSAL_NO, _("No Dismissals Allowed")),
        (DISMISSAL_SESSION, _("Session Only Dismissal")),
        (DISMISSAL_PERMANENT, _("Permanent Dismissal Allowed"))
    ]
    title = models.CharField(_("title"), max_length=50)
    content = models.TextField(_("content"))
    creator = models.ForeignKey(User, verbose_name=_("creator"))
    creation_date = models.DateTimeField(_("creation_date"), default=timezone.now)
    site_wide = models.BooleanField(_("site_wide"), default=False)
    members_only = models.BooleanField(_("members only"), default=False)
    dismissal_type = models.IntegerField(choices=DISMISSAL_CHOICES, default=DISMISSAL_SESSION)
    publish_start = models.DateTimeField(_("publish_start"), default=timezone.now)
    publish_end = models.DateTimeField(_("publish_end"), blank=True, null=True)

    objects = AnnouncementManager()

    #@models.permalink
    def get_absolute_url(self):
        return reverse("announcement_detail", args=[str(self.pk)])

    def dismiss_url(self):
        if self.dismissal_type != Announcement.DISMISSAL_NO:
            return reverse("announcement_dismiss", args=[self.pk])

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name=_("Announcement")
        verbose_name_plural = _("Announcements")


class Dismissal(models.Model):
    user = models.ForeignKey(User, related_name="announcement_dimissals")
    announcement = models.ForeignKey(Announcement, related_name="dismissals")
    dismissed_at = models.DateTimeField(default=timezone.now)

#
def current_announcements_for_request(request, **kwargs):
    """A helper function to get the current announcements based on some data from
    the HttpRequest.

    If request.user is authenticated then allow the member only announcements to be
    returned.

    Exclude announcements that have already been viewed by the user based on the
    ``excluded_announcements`` session variable."""
    defaults = {}
    if request.user.is_authenticated():
        defaults["for_members"] = True
    defaults["exclude"] = request.session.get("excluded_announcements", set())
    defaults.update(kwargs)
    return Announcement.objects.current(**defaults) #[:2]
