
from django.db import models
from taggit.managers import TaggableManager


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(db_index=True, default=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    tags = TaggableManager()
    images = models.ManyToManyField('gallery.PhotoUrl', blank=True)

    def __unicode__(self):
        return self.title

    def brief(self):
        if self.text.startswith("reStructured"):
              return self.text.replace('\r', '').split('Abstract\n========\n\n')[1].replace('==', '').split('\n')[0][:150] + '...'
        return self.text.replace('\r', '')\
                        .replace('Abstract\n========', '')\
                        .replace('## Abstract', '')[:150] + '...'
    def slugify(self):
        return self.title.replace(' ', '_')

    def get_absolute_url(self):
        return '/blog/%i' % self.id
