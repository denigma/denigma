from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Image(models.Model):
    url = models.CharField(max_length=128)
    uploaded = models.DateTimeField()
    user = models.ForeignKey(User, default=2, related_name='uploader')
    artist = models.ForeignKey(User, null=True, blank=True)
    
    def save(self):
        self.uploaded = datetime.now()
        models.Model.save(self)

    def __unicode__(self):
        return self.url.split('/')[-1]

    def get_absolute_url(self):
        return self.url

    def name(self):
        return self.url.split('/')[-1].split('/')[0]

    class Meta():
        verbose_name = _('Image')
        verbose_name_plural = _('Images')