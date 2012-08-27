from django.db import models
from taggit.managers import TaggableManager


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    def brief(self):
        return self.text[:150] + '...'






