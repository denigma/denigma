# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import signals
from django.contrib.auth.models import User
#from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager

try: 
    from articles.manager import referencing
except ImportError:
   print("No article manager for references available.")

from handlers import notify_admin


class TimeTrack(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        abstract = True


class Post(TimeTrack):
    """The fundamental textual data-structure of Denigma."""

    published = models.BooleanField(_('published'), db_index=True, default=True)
    creator = models.ForeignKey(User, null=True, blank=True, related_name='created_by')
    updater = models.ForeignKey(User, null=True, blank=True, related_name='updated_by')
    title = models.CharField(_('title'), max_length=250)
    text = models.TextField(_('text'))
    tags = TaggableManager(_('tags'))
    url = models.CharField(_('URL'), max_length=100, blank=True, null=True,
        help_text="Example: '/future/projects/'. Make sure to have leading and trailing slashes.")
    images = models.ManyToManyField('media.Image', blank=True)

    def save(self, *args, **kwargs):
        """Triggers the generation of referenced document if article is marked
        with reStructured referenced."""
        if self.text.startswith("reStructured referenced") and self.pk and\
           "article" in [tag.name for tag in self.tags.all()]:
            referencing(self)
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.url:
            return self.url
        else:
            return '/blog/%i' % self.id

    def slugify(self):
        return self.title.replace(' ', '_')

    def brief(self):
        if self.text.startswith("reStructured"):
            return self.text.replace('\r', '').split('Abstract\n========\n\n')[1].replace('==', '').split('\n')[0][:150] + '...'
        return self.text.replace('\r', '')\
               .replace('Abstract\n========', '')\
               .replace('## Abstract', '')[:150] + '...'


    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Comment(TimeTrack):
    post = models.ForeignKey(Post, related_name='comments')
    text = models.TextField()
    maker = models.ForeignKey(User, blank=True, null=True, related_name="made_by")


signals.post_save.connect(notify_admin, sender=Post)
#23456789112345678921234567893123456789412346789512345678961234567897123456789   
