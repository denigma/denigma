# -*- coding: utf-8 -*-
from django.db import models
from taggit.managers import TaggableManager

try: 
    from articles.manager import referencing
except ImportError:
   print("No article manager for references available.")


class Post(models.Model):
    """The fundamental textual datastructure of Denigma."""
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

    def save(self, *args, **kwargs):
        """Triggers the generation of referened document if article is marked
        with reStructured referenced."""
        if self.text.startswith("reStructured referenced") and self.pk and\
           "article" in [tag.name for tag in self.tags.all()]:
            referencing(self)
        super(Post, self).save(*args, **kwargs)

#23456789112345678921234567893123456789412346789512345678961234567897123456789   
