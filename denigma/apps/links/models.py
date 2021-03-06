# -*- coding: utf-8 -*-
"""Modelling links."""
from datetime import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

#from mptt.models import MPTTModel, TreeForeignKey
import tagging
from tagging.fields import TagField
from tagging.models import Tag

#from south.modelinspector import add_introspection_rules
#add_introspection_rules([])
from managers import ResearchManager



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

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.slug:
                self.slug = slugify(self.title)
        return super(Category, self).save(*args,**kwargs)

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
    categories = models.ManyToManyField('data.Entry',  related_name='links', blank=True, null=True)
    countries = models.ManyToManyField('Country', verbose_name=_("Countries of residence"),
        blank=True, null=True)
    visibility = models.BooleanField(_('visibility'), default=True)
    ordering = models.IntegerField(_('ordering'), default=100)
    creation = models.DateTimeField(_('created'), auto_now_add=True)
    publication_start = models.DateTimeField(_('publication start'),
                                             default=datetime.now)
    publication_end = models.DateTimeField(_('publication end'),
                                           default=datetime(2042, 3, 15))
    site = models.ForeignKey(Site, verbose_name=_('site'), default=get_site) # Can also be ManyToMany()
    #sites = models.ManyToManyField(Site, default=get_site)
    objects = models.Manager()
    published = LinkPublishedManager()
    contacts = models.ManyToManyField('experts.Profile', blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    tags = TagField()

    #research = ResearchManager()

    def __unicode__(self):
        return self.title


#    def set_tags(self, tags):
#        Tag.objects.update_tags(self, tags)

#    def get_tags(self, tags):
#        return Tag.objects.get_for_object(self, tags)

    def get_absolute_url(self):
        return reverse('link', args=[self.pk])

    def save(self, *args, **kwargs):
        self.url = self.url.strip() # Strips away leading and trailing spaces.
        super(Link, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        ordering = ('title',)


class Country(models.Model):
    abbreviation = models.CharField(max_length=10)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name  # , "%s" % ((%s) self.abbreviation

#tagging.register(Link)
