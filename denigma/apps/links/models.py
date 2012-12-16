# -*- coding: utf-8 -*-
"""Modelling links."""
from datetime import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.urlresolvers import reverse
#from mptt.models import MPTTModel, TreeForeignKey

from tagging.fields import TagField
from tagging.models import Tag


class LinkPublishedManager(models.Manager):
    """Link published manager."""
    def get_query_set(self):
        now = datetime.now()
        return super(LinkPublishedManager, self).get_query_set().filter(
            publication_start__lte=now, publication_end__gt=now,
            site=Site.objects.get_current(), visibility=True).order_by('ordering', '-creation')


class Category(models.Model): #MPTTModel
    """Category Model."""
    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), help_text=_('Used for the URLs'))
    description = models.TextField(_('description'), blank=True)
#    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('links-category', args=[self.slug])

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('title',)

#    class MPTTMeta:
#        order_insertion_by = ['title']

def get_site():
    return Site.objects.get(domain='denigma.de')

class Link(models.Model):
    """Link Model."""
    title = models.CharField(_('title'), max_length=150, default=None)
    language = models.CharField(_('language'), max_length=2,
                                choices=settings.LANGUAGES, default='en')
    url = models.URLField(_('url'), default=None)
    description = models.TextField(_('description'), blank=True)
    category = models.ManyToManyField(Category, verbose_name=_('category'),
                                      null=True)
    visibility = models.BooleanField(_('visibility'), default=True)
    ordering = models.IntegerField(_('ordering'), default=100)
    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    publication_start = models.DateTimeField(_('publication start'),
                                             default=datetime.now)
    publication_end = models.DateTimeField(_('publication end'),
                                           default=datetime(2042, 3, 15))
    site = models.ForeignKey(Site, verbose_name=_('site'), default=get_site) # Can also be ManyToMany()
    objects = models.Manager()
    published = LinkPublishedManager()
    tags = TagField()

    def __unicode__(self):
        return self.title

#    def set_tags(self, tags):
#        Tag.objects.update_tags(self, tags)

#    def get_tags(self, tags):
#        return Tag.objects.get_for_object(self, tags)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        ordering = ('title',)
        
#tagging.register(Link)
