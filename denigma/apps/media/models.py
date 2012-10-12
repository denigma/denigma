from datetime import datetime
from django.db import models


class Image(models.Model):
    url = models.CharField(max_length=128)
    uploaded = models.DateTimeField()
    
    def save(self):
        self.uploaded = datetime.now()
        models.Model.save(self)

    def __unicode__(self):
        return self.url.split('/')[-1]

    def name(self):
        return self.url.split('/')[-1].split('/')[0]

    class Meta:
        verbose_name = u"Photo URL"
        # For now leave table name as is:
        #db_table = 'gallery_photourl'
        #db_table = 'media_photourl'