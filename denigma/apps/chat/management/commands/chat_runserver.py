from django.core.management import call_command
from gevent import spawn

from denigma.apps.chat.management.commands import chatting


class Command(chatting.Command):
    def handle(self, *args, **options):
        spawn(lambda: call_command('runserver', *args))
        super(Command, self).handle(*args, **options)