from django.conf import settings


TRACK_ACTIVITIES = getattr(settings, 'TRACK_ACTIVITIES', True)

TRACK_IGNORE_URLS = getattr(settings, 'TRACK_IGNORE_URLS', (
    r'^(favicon\.ico|robots\.txt)$',
    r'^(media/img/favicon.ico)$',
    r'^(admin/jsi18n)',
))