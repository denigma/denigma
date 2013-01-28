from django.db import models
from django.utils.translation import ugettext_lazy as _

from chat.client import color


class Message(models.Model):
    """An chat message logged by the DjangoBot from the
    ``run_chat`` management command."""
    nickname = models.CharField(_("Nickname"), max_length=100)
    message = models.TextField(_('Text'), max_length=100) #text
    server = models.CharField(_("Server"), max_length=100)
    channel = models.CharField(_("Channel"), max_length=100)
    time = models.DateTimeField(_("Time"), auto_now_add=True)
    join_or_leave = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ('time',)

    def __unicode__(self):
        return "[%s] %s%s %s: %s" % (self.time, self.server,
                                     self.channel, self.nickname,
                                     self.short())

    @models.permalink
    def get_absolute_url(self):
        kwargs = {
            "year": self.time.year,
            "month": self.time.month,
            "day": self.time.day,
        }
        return ("chat_day", (), kwargs)

    def short(self):
        return self.message[:50] #text
    short.short_description = _("Text")

    def color(self):
        return color(self.nickname)
