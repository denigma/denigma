# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
#from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager


try: 
    from articles.manager import referencing
except ImportError:
   print("No article manager for references available.")


class Post(models.Model):
    """The fundamental textual data-structure of Denigma."""
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    published = models.BooleanField(_('published'), db_index=True, default=True)
    title = models.CharField(_('title'), max_length=250)
    text = models.TextField(_('text'))
    tags = TaggableManager(_('tags'))
    url = models.CharField(_('URL'), max_length=100, blank=True, null=True,
        help_text="Example: '/future/projects/'. Make sure to have leading and trailing slashes.")
    images = models.ManyToManyField('gallery.PhotoUrl', blank=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
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
        if hasattr(self, 'url') and self.url:
            return self.url
        else:
            return '/blog/%i' % self.id

    def save(self, *args, **kwargs):
        """Triggers the generation of referenced document if article is marked
        with reStructured referenced."""
        if self.text.startswith("reStructured referenced") and self.pk and\
           "article" in [tag.name for tag in self.tags.all()]:
            referencing(self)
        if hasattr(self, 'url'):
            if self.url.startswith('/'):
                self.url = settings.BASE_URL + self.url
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

#23456789112345678921234567893123456789412346789512345678961234567897123456789   
