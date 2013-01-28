from gevent.monkey import patch_all
patch_all()

from logging import getLogger, StreamHandler

from django.core.management.base import BaseCommand

from chat.conf import settings
from chat.models import Message


class ModelLogger(StreamHandler):
    """"Logging handler that saves an IRC message to the DB."""
    def emit(self, record):
        Message.objects.create(server=record.server,
                               channel=record.channel,
                               nickname=record.nickname,
                               message=record.msg, #text
                               join_or_leave=record.join_or_leave)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + tuple(settings.option_list)

    def handle(self, *args, **options):
        getLogger('irc.message').addHandler(ModelLogger())
        settings.parse_args()
        from denigma.apps.chat.server import serve_forever
        serve_forever(django=True)
