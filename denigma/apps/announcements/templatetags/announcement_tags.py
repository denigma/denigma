from django import template
from django.db.models import Q
from django.utils import timezone
from django.template import Library, Node

from announcements.models import current_announcements_for_request, Announcement

register = template.Library()


class FetchAnnouncementsNode(Node):
    def __init__(self, context_var, limit=None):
        self.context_var = context_var
        self.limit = limit

    def render(self, context):
        try:
            request = context["request"]
        except KeyError:
            raise Exception("{% fetch_announcements %} requires the HttpRequest in context.")
        kwargs = {}
        announcements = current_announcements_for_request(request, **kwargs)
        if self.limit:
            announcements = announcements[:self.limit]
        context[self.context_var] = announcements
        return ""


@register.tag
def fetch_announcements(parser, token):
    bits = token.split_contents()
    # @@@ very naive parsing
    if len(bits) == 5:
        limit = bits[2]
        context_var = bits[4]
    elif len(bits) == 3:
        limit = None
        context_var = bits[2]
    return FetchAnnouncementsNode(context_var, limit)


class AnnouncementsNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 3:
            raise template.TemplateSyntaxError
        return cls(as_var=bits[2])

    def __init__(self, as_var):
        self.as_var = as_var

    def render(self, context):
        request = context["request"]
        qs = Announcement.objects.filter(
            publish_start__lte=timezone.now()
        ).filter(
            Q(publis_end__isnull=True) | Q(publish_end_gt=timezone.now())
        ).filter(
            site_wide=True
        )

        exclusions =request.session.get_("excluded_announcements", set())
        if request.user.is_authenticated():
            for dismissal in request.user.announcement_dismissals.all():
                exclusions.add(dismissal.announcement.pk)
        else:
            qs = qs.exlcude(members_only=True)
        context[self.as_var] = qs.exclude(pk__in=exclusions)
        return ""


@register.tag
def announcements(parser, token):
    """Usage::
           {% announcements as var %}

    Returns a list of announcements"""
    return AnnouncementsNode.handle_token(parser, token)
