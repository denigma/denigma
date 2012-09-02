
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
        return self.text[:150] + '...'

    def slugify(self):
        return self.title.replace(' ', '_')




