from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4


class PastedItem(models.Model):
    """An item that was pasted."""
    uuid = models.CharField(_('identifier'), max_length=36, unique=True)
    text = models.TextField(_('text'))
    in_response_to = models.ForeignKey('self', related_name='response',
        blank=True, null=True, verbose_name=_('in response to'))
    user = models.ForeignKey(User, related_name="pasted_items",
       verbose_name=_('user'))
    pasted_at = models.DateTimeField(_('pasted at'), auto_now_add=True)

    def __unicode__(self):
        return self.uuid

    @property
    def short(self):
        return self.text[:100]

    def save(self):
        if not self.uuid:
            self.uuid = str(uuid4()) # Random so it can't be easily guessed.
        super(PastedItem, self).save()

    def get_absolute_url(self):
        return ('pastebin_detail', (), { 'uuid': self.uuid })
    get_absolute_url = models.permalink(get_absolute_url)
