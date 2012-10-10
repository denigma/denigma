# -*- coding: utf-8 -*-
print("Denigma's fundamental data structure here!")
from copy import deepcopy

from django.db import models, IntegrityError, transaction
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save, m2m_changed
from managers import EntryManager
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

import signals
import handlers

from home.signals import message_sent
from django.utils.translation import ugettext_lazy as _

try:
    from blog.models  import Post # To be replaced by data entry model
except Exception as e:
    print ("data.models: %s" % e)


class Title(MPTTModel):
    """Abstract title with capability of auto-generating a slug."""
    title = models.CharField(_('title'), max_length=255) #, unique=True?
    slug = models.SlugField(_('slug'), max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """Based on the  Tag save() method in django-taggit, this method simply stores a
        slugfield version of the title, ensuring that the unique constraint is observed.
        """
        #print("%s title model save() called" % self.__class__)
        self.slug = slug = slugify(self.title)
        i = 0
        while True:
            try:
                savepoint = transaction.savepoint()
                res = super(Title, self).save(*args, **kwargs)
                transaction.savepoint_commit(savepoint)
                return res
            except IntegrityError as e:
                transaction.savepoint_rollback(savepoint)
                i += 1
                self.slug = '%s_%d' % (slug, i)
                print e, self.slug

    class Meta:
        abstract = True


class Content(Title):
    """Data content following the TTT and I princip."""
    #title = models.CharField(max_length=250) # Tag?
    text = models.TextField(_('text'))
    tags = TaggableManager(_('tags'))
    tagged = models.ManyToManyField('Tag', verbose_name=_('tagged'), blank=True, null=True) # M2M to Entry? #tags = TaggableManager() # #Categories?
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.CharField(_('url'), max_length=255, blank=True, null=True) #,
    images = models.ManyToManyField('gallery.PhotoUrl', blank=True, verbose_name=_('images'))

    def save(self, *args, **kwargs):
        print("%s content model save() called" % self.__class__)
        super(Title, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} {1} {2} {3}".format(self.title, len(self.text),
            len(self.tags.all()), len(self.images.all()))

    def brief(self, limit=150):
        return self.text[:limit] + '...'

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['title']


class Entry(Content):
    """A database entry containing the actual data content and meta data."""
    # Meta data:
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    #pub_data = models.DateTimeField(_('publication date'), blank=True, null=True)

    # User track:
    creator = models.ForeignKey(User, related_name=_('creator'), blank=True, null=True, verbose_name=_('creator')) # M2M allow more than one creator? #_
    updates = models.ManyToManyField(User, through='Change', verbose_name=_('updates')) # changed changes? #_('updates'),
    publisher = models.ForeignKey(User, related_name=_('publisher'), blank=True, null=True) # M2M? #_('publisher'),
    published = models.BooleanField(_('published'), db_index=True, default=True) # DateTimeField()?
    original = None
    tagged_changed = []

    objects = EntryManager()

    def __init__(self, *args, **kwargs):
        """Keeps a copy of its original state."""
        #print("args, kwargs: %s %s" % (args, kwargs))
        if args:
            args = list(args)
            for index, arg in enumerate(args[:]):
                if isinstance(arg, User):
                    self.user = arg
                    args.remove(arg)
                elif isinstance(arg, Post):
                    self.post = arg
                    args.remove(arg)
                    if hasattr(self.post, 'user'):
                        self.user = self.post.user
            args = tuple(args)

        if kwargs:
            if "post" in kwargs:
                self.post = kwargs['post']
                del kwargs['post']
            if "user" in kwargs:
                self.user = kwargs['user']
                del kwargs['user']

        super(Entry, self).__init__(*args, **kwargs)
        self.original = deepcopy(self)

    def save(self, *args, **kwargs):
        #signals.tags_added.send("siste", tags="tags", instance="instance")
        self.Change = Change
        #print("entry model save() called.")
        if not self.pk:
            self.creator = self.creator or self.user
            if self.published:
                self.publisher = self.publisher or self.user
            super(Content, self).save(*args, **kwargs)
            if hasattr(self, 'post'): # Get initial data from post if available.
                post = self.post
                try:
                    self.created = post.created
                    self.updated = post.updated
                    self.published = post.published
                    self.title = post.title
                    self.text = post.text
                    #self.tags = post.tags
                    tags = post.tags.all()
                    if tags:
                        signals.tags_added.send("Post", tags=tags, instance=self)
                        #tags = [Tag(name=tag.name) for tag in tags]
                    for tag in tags:
                        tag, created = Tag.objects.get_or_create(name=tag.name)
                        #print tag
                        self.tagged.add(tag)
                        #self.tagged =  Tag.objects.all()
                    self.images = post.images.all()

                    #tags = self.post.tags.all()
                    #for tag in tags:
                    #    self.tags.add(tag.name)
                    #print("Init tag addition: %s" % self.tags.all())

                except Exception as e:
                    print("data.models.Entry.save: %s (%s %s)" % (e, post.pk, post.title))
            initial = Change(title=self.title, text=self.text, url=self.url, of=self, by=self.user)
            #initial.tags = self.tags.all()
            self.tags_pre_clear = [tag.name for tag in self.tags.all()]
        else:
            changes = []
            #print("Title %s vs. %s" % (self.title, self.original.title))
            if self.title != self.original.title:
                changes.append('title')
            if self.slug != self.original.slug:
                changes.append('slug')
            if self.text != self.original.text:
                changes.append('text')
            if self.url != self.original.url:
                changes.append('urls')

            if changes:
                print(changes)
                self.change = Change(title=self.title, slug=self.slug, text=self.text, url=self.url,#, tags=self.tags.all(), images=self.images.all(),
                    of=self, by=self.user)

                self.change.save()
                self.change.images.add(*self.images.all())
                self.change.tags.add(*self.tags.all())
                self.change.tagged.add(*self.tagged.all())

        super(Content, self).save(*args, **kwargs)
        self.tags_pre_clear = [tag.name for tag in self.tags.all()]

    def __unicode__(self):
        return "{0} - {1} ({2})".format(self.title, self.created.date(), self.created.time())

    def get_absolute_url(self):
        return self.url or u"/data/entry/%s" % self.pk

    class Meta:
        verbose_name_plural = "Entries"


class Change(Content):
    """A snapshot change of a data entry."""
    of = models.ForeignKey(Entry, related_name='entry', verbose_name=_('of')) # what #
    by = models.ForeignKey(User, related_name='user', verbose_name=_('by'))   # who #
    at = models.DateTimeField(_('at'), auto_now=True)    # when #

    def save(self, *args, **kwargs):
        #print("change model save() called.")
        super(Content, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{0} changed "{1}" on {2} {3}'.format(self.by, self.of.title,
            self.at.date(), self.at.time())

    def diff(self):
        """returns any differences from the previous revision."""
        # Query changes for the privious revision via the id time
        #SELECT * FROM changes WHERE of == self.of LIMIT self.id
        #previous = Change.objects.filter(Q(of=self.of) & id<=self.id)[-1]
        #for
        #return self.title - self.of.titl
        for letter in previous.text:
            if letter not in self.text:
                print("-"+letter)


class Tag(models.Model):
    """A category tag modeling a namespace."""
    name = models.CharField(_('name'), max_length=255, unique=True)
    synonyms = models.ManyToManyField('self', blank=True, verbose_name=_('synonyms'))

    def __unicode__(self):
        return self.name


class Relationship(models.Model):
    """A relationship of an entry (source) to and entry (target) by and entry (type)."""
    fr = models.ForeignKey('Entry', related_name=_("source"), verbose_name=_('from'))
    be = models.ForeignKey('Entry', related_name=_("type"), verbose_name=_('be'))
    to = models.ForeignKey('Entry', related_name=_("target"), verbose_name=_('to'))

    def __unicode__(self):
        return "{0} -{1}-> {2}".format(self.fr.title, self.be.title, self.to.title)

    class Meta:
        abstract = True


class Relation(Relationship):
    """A relationship of an entry (source) to and entry (target) by and entry (type)."""
    # Meta data:
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)

    # User track:
    creator = models.ForeignKey(User, related_name=_('maker'), blank=True, null=True, verbose_name=_('maker')) # M2M allow more than one creator? #_
    updates = models.ManyToManyField(User, through='Alteration', verbose_name=_('updates')) # changed changes? #_('updates'),

    original = None

    def __init__(self, *args, **kwargs):
        super(Relation, self).__init__(*args, **kwargs)
        self.original = deepcopy(self)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = self.creator or self.user
            super(Relationship, self).save(*args, **kwargs)
            alteration = Alteration(fr=self.fr, be=self.be, to=self.to, of=self, by=self.user)
            alteration.save()
        else:
            alterations = []
            if self.fr != self.original.fr:
                alterations.append(self.fr)
            if self.be != self.original.be:
                alterations.append(self.be)
            if self.to != self.original.to:
                alterations.append(self.to)

            #print "From: ", self.fr, self.original.fr
            #print "Be: ", self.be, self.original.be
            #print "To: ", self.to, self.original.to

            if alterations:
                print(alterations)
                alteration = Alteration(fr=self.fr, be=self.be, to=self.to, of=self, by=self.user)
                alteration.save()

            super(Relationship, self).save(*args, **kwargs)


class Alteration(models.Model):
    """Any alteration of relationships."""
    fr = models.ForeignKey('Entry', related_name="source_entry", verbose_name=_('from'))
    be = models.ForeignKey('Entry', related_name="type_of", verbose_name=_('be'))
    to = models.ForeignKey('Entry', related_name="target_entry", verbose_name=_('to'))

    of = models.ForeignKey(Relation, related_name='relationship', verbose_name=_('of')) # what
    by = models.ForeignKey(User, related_name='person', verbose_name=_('by'))   # who
    at = models.DateTimeField(_('at'), auto_now=True)    # when

    def __unicode__(self):
        return "{0} {1} {2} by {3} at {4}".format(self.fr, self.be, self.to, self.of, self.by, self.at)


class EntryDummy(object):
    def __init__(self, title=None, text=None, tags=None, images=None, urls=None):
        self.title = title
        self.text = text
        self.tags = tags
        self.images = images
        self.urls = urls


# Signals:
#request_finished.connect(handlers.request_finished)
#pre_save.connect(handlers.saving_model, sender=Entry)
#post_save.connect(handlers.model_saved, sender=Entry)
#reversion.pre_revision_commit.connect(handlers.pre_revision, sender=Entry)
#reversion.post_revision_commit.connect(handlers.post_revision, sender=Entry)
m2m_changed.connect(handlers.changed_tags, sender=Entry.tags.through)
m2m_changed.connect(handlers.changed_tagged, sender=Entry.tagged.through)
m2m_changed.connect(handlers.changed_images, sender=Entry.images.through)
message_sent.connect(handlers.message_sent)

signals.tags_added.connect(handlers.adding_tags)

#2345678911234567892123456789312345678941234567895123456789612345678961234567897123456789