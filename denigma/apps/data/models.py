# -*- coding: utf-8 -*-
#print("Denigma's fundamental data structure here!")
import re
from copy import deepcopy

from django.db import models, IntegrityError, transaction
from django.db.models import Q
from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save, m2m_changed
#from managers import EntryManager
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from taggit.managers import TaggableManager
from mptt.models import MPTTModel, TreeForeignKey

from meta.diff.diff_match_patch import diff_match_patch
dmp = diff_match_patch()

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
                #transaction.savepoint_rollback(savepoint)
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
    categories = models.ManyToManyField('Category', blank=True, null=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.CharField(_('url'), max_length=255, blank=True, null=True) #,
    images = models.ManyToManyField('media.Image', blank=True, verbose_name=_('images'))

    def save(self, *args, **kwargs):
        #print("%s content model save() called" % self.__class__)
        super(Title, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{0} {1} {2} {3}".format(self.title, len(self.text),
            len(self.tags.all()), len(self.images.all()))

    def brief(self, limit=150):
        rc = re.compile(r'={2,}\r\n.{2,}\r\n={2,}')
        match = re.match(rc, self.text)
        if match:
            #print match.group(0)
            text = self.text.replace(match.group(0), '')
        else:
            text = self.text
        return text[:int(limit)].replace('Abstract\r\n========', '') + '...'

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['title']


class Entry(Content):
    """A database entry containing the actual data content and meta data."""
    # Meta data:
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    pub_date = models.DateTimeField(_('publication date'), blank=True, null=True)

    #relations = models.ManyToManyField('self', through='Relation', symmetrical=False, related_name='relation')#, blank=True, null=True)

    # User track:
    creator = models.ForeignKey(User, related_name=_('entries'), blank=True, null=True, verbose_name=_('creator')) # M2M allow more than one creator? #_
    updates = models.ManyToManyField(User, related_name='updated_entries', through='Change', verbose_name=_('updates')) # changed changes? #_('updates'),
    publisher = models.ForeignKey(User, related_name=_('published_entries'), blank=True, null=True) # M2M? #_('publisher'),
    published = models.BooleanField(_('published'), db_index=True, default=True) # DateTimeField()?
    original = None
    tagged_changed = []
    comment = ''

    #objects = EntryManager()

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

    def get_parent_change(self):
        parents = Change.objects.filter(of=self.parent)
        if parents:
            parent = parents[0]
        else:
            parent = None
            ## Alternative one-liners to fetch parent:
            #parent = next(iter(Change.objects.filter(of=self.parent), None))
            #parent, = Change.objects.filter(of=self.parent) or [None]
        return parent

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
                    parent = None
                    self.change = Change(title=self.title, text=self.text, url=self.url, of=self,
                        by=self.user, comment=self.comment, parent=parent, initial=True)
                    self.change.save()

                    tags = post.tags.all()
                    if tags:
                        signals.tags_added.send("Post", tags=tags, instance=self)
                    for tag in tags:
                        tag, created = Tag.objects.get_or_create(name=tag.name)
                        self.tagged.add(tag)
                        #self.tagged =  Tag.objects.all()
                    self.tags_pre_clear = [tag.name for tag in self.tags.all()]

                    # Deactivate.

                    self.images = post.images.all()

                except Exception as e:
                    print("data.models.Entry.save: %s (%s %s)" % (e, post.pk, post.title))

            else:
                print("data.models.Entry.save(): Searching for parent")
                parent = self.get_parent_change()
                self.change = Change(title=self.title, text=self.text, url=self.url,
                    of=self, by=self.user, comment=self.comment, parent=parent, initial=True)
                #print("data.models.Entry.save(): self.change = %s" % self.change)
                #initial.tags = self.tags.all()
                self.change.save()
                self.tags_pre_clear = [tag.name for tag in self.tags.all()]
                self.categories_pre_clear = [category.name for category in
                                             self.categories.all()]

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
            if self.parent != self.original.parent:
                changes.append('parent')

            if changes:
                #print(changes)
                #parent = Change.objects.filter(of=self.parent)
                parent = self.get_parent_change()
                self.change = Change(title=self.title, slug=self.slug, text=self.text, url=self.url,
                    of=self, by=self.user, comment=self.comment, parent=parent)

                self.change.save()
                self.change.images.add(*self.images.all())
                self.change.tags.add(*self.tags.all())
                #self.change.tagged.add(*self.tagged.all())
                self.change.categories.add(*self.categories.all())

        super(Content, self).save(*args, **kwargs)
        self.tags_pre_clear = [tag.name for tag in self.tags.all()]
        self.categories_pre_clear = [category.name for category in self.categories.all()]

    def __unicode__(self):
        return self.title
        #return "{0} - {1} ({2})".format(self.title, self.created.date(), self.created.time())

    def get_absolute_url(self):
        if not self.published:
            return reverse('article', args=[self.title.replace(' ', '_')])
        # or "rest" in [tag.name for tag in self.tags.all()]:
        #    return reverse('article', args=[self.title.replace(' ', '_')])
        return self.url or reverse('detail-entry', args=[self.slug]) #return self.url or u"/data/entry/%s" % self.pk

    def get_update_url(self):
        return reverse('update-entry', args=[self.slug])

    def get_fields(self):
        """Displays only model fields that are non-empty."""
        return [(field.name, field.value_to_string(self)) for field in Entry._meta.fields if field.value_to_string(self) is not None]

    def detail(self):
        return reverse('detail-entry',args=[self.slug])

    def content(self):
        return self.text + "  <b><a href='/data/entry/update/%s'>o</a></b>" % self.slug

    def content_link(self):
        return self.text + "\n\n  <b><a href='/data/entry/update/%s'>o</a></b>" % self.slug

    def is_rest(self):
        """returns True if entry is tagged to be fully encoded in reStructuredText."""
        if "rest" in [tag.name for tag in self.tags.all()] or "reST" in [category.name for category in self.categories.all()]:
            return True
        return False

    class Meta:
        verbose_name_plural = "Entries"


class Change(Content):
    """A snapshot change of a data entry."""
    of = models.ForeignKey(Entry, related_name='entry', verbose_name=_('of')) # what #
    by = models.ForeignKey(User, related_name='user', verbose_name=_('by'))   # who #
    at = models.DateTimeField(_('at'), auto_now=True)    # when #
    initial = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, blank=True, null=True)

    previous_version = None

    def save(self, *args, **kwargs):
        #print("change model save() called.")
        super(Content, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.initial:
            action = 'initialized'
        else:
            action = 'changed'
        return u'{0} {1} "{2}" on {3} {4}'.format(self.by, action, self.of.title,
            self.at.date(), self.at.time())

    def get_absolute_url(self):
        return reverse('detail-change', args=[self.pk])

    def previous(self):
        if self.previous_version:
            return self.previous_version
        try:
            self.previous_version = Change.objects.filter(Q(of=self.of) & Q(pk__lt=self.pk)).order_by('-pk')[0]
            return  self.previous_version
        except:
            return ''

    def diff(self):
        """returns any differences from the previous revision."""
        # Query changes for the privious revision via the id time
        #SELECT * FROM changes WHERE of == self.of LIMIT self.id
        #print("data.models.change.diff %s" % self)
        #from meta.helpers import generate_patch_html
        if self.initial:
            #print("initial")
            return ''
        #print("change")
        previous = self.previous()
        differences = []
        if previous.title != self.title:
            #diff = dmp.diff_main(previous.title, self.title)
            #patch = dmp.patch_make(diff)
            differences.append('Title') # (%s)' % dmp.patch_toText(patch)
        if  previous.text != self.text:
            #diff = dmp.diff_main(previous.text, self.text)
            #patch = dmp.patch_make(diff)
            differences.append('Text') # (%s)' % dmp.patch_toText(patch))
        if [tag.name for tag in previous.tags.all()] != [tag.name for tag in self.tags.all()]:
            differences.append('Tags')
        previous_categories = [category.name for category in previous.categories.all()]
        self_categories = [category.name for category in self.categories.all()]
        if  previous_categories != self_categories:
            differences.append('Categories')
        if  previous.url != self.url and not (not previous.url and not self.url): # In the case the url are '' and None.
            differences.append('URL')
        if [image.name for image in previous.images.all()] != [image.name for image in self.images.all()]:
            differences.append('Images')
        #print previous.parent, self.parent
        if previous.parent != self.parent:
            #print previous.parent != self.parent
            #print previous.parent, self.parent
            differences.append('Parent')

        return ", ".join(differences)

    def difference(self, field='title'):
        if self.initial: return ''
        previous = self.previous()
        differences = []
        if self.title != previous.title:
            diffs = dmp.diff_main(previous.title, self.title)
            return mark_safe(dmp.diff_prettyHtml(diffs))
        return ''

    def differences(self):
        if self.initial: return ''
        previous = self.previous()
        changes = EntryDummy()
        differences = []
        if previous.title != self.title:
            diffs = dmp.diff_main(previous.title, self.title)
            changes.title = mark_safe(dmp.diff_prettyHtml(diffs))
        else:
            changes.title = self.title
        if previous.text != self.text:
            diffs = dmp.diff_main(previous.text, self.text)
            changes.text = mark_safe(dmp.diff_prettyHtml(diffs))
        else:
            changes.text = self.text
        if previous.url != self.url and not (not previous.url and not self.url):
            if not previous.url: previous.url = ''
            if not self.url: self.url = ''
            diffs = dmp.diff_main(previous.url, self.url)
            changes.url = mark_safe(dmp.diff_prettyHtml(diffs))
        else:
            changes.url = self.url

        # Tags:
        previous_tags= set([tag.name for tag in previous.tags.all()])
        self_tags = set([tag.name for tag in self.tags.all()])
        if previous_tags != self_tags:
            changes.tags_added = list(self_tags - previous_tags)
            changes.tags_removed = list(previous_tags - self_tags)
            changes.tags = list(previous_tags & self_tags)
        else:
            changes.tags_added = changes.tags_removed = []
            changes.tags = self_tags
        print previous_tags, self_tags

        # Categories:
        previous_categories = set([category.name for category in previous.categories.all()])
        self_categories = set([category.name for category in self.categories.all()])
        if previous_categories != self_categories:
            changes.categories_added = list(self_categories - previous_categories)
            changes.categories_removed = list(previous_categories - self_categories)
            changes.categories = previous_categories & self_categories
            changes.categories_changed = True
        else:
            changes.categories_added = changes.categories_removed = []
            changes.categories = self_categories
            changes.categories_changed = False
        print("Categories: %s %s %s" % (previous_categories, self_categories, self.categories))

        # Parent:
        changes.previous_parent = previous.parent
        #print("data.models: Parent")
        #print previous.parent, self.parent
        #previous.parent == self.parent
        if previous.parent != self.parent:
            changes.parent_changed = True
        else:
            changes.previous_parent = False
        changes.parent = changes.current_parent = self.parent

        print("Previous, current, parent: %s %s %s" % (changes.previous_parent, changes.current_parent, self.parent))

        # Images:
        previous_images = set([image.name() for image in previous.images.all()])
        self_images = set([image.name() for image in self.images.all()])
        if previous_images != self_images:
            changes.images_added = list(self_images - previous_images)
            changes.images_removed = list(previous_images - self_images)
            changes.images = previous_images & self_images
            changes.images_changed = True
        else:
            changes.images_added = changes.images_removed = []
            changes.images = self_images
            changes.images_changed = False
        print changes.images_added, changes.images_removed

#        if [tag.name for tag in previous.tagged.all()] != [tag.name for tag in self.tagged.all()]:
#            differences.append('Tagged')
        return changes

        #for
#        #return self.title - self.of.title
#        for letter in previous.text:
#            if letter not in self.text:
#                print("-"+letter)


#class RelationshipType(models.Model):
#    name = models.CharField(max_length=255, unique=True)
#    description = models.TextField(blank=True, null=True)

class Relationship(models.Model):
    """A relationship of an entry (source) to and entry (target) by and entry (type)."""
    fr = models.ForeignKey('Entry', related_name=_("source"), verbose_name=_('from'))
    be = models.ForeignKey('Entry', related_name=_("type"), verbose_name=_('be'))
    to = models.ForeignKey('Entry', related_name=_("target"), verbose_name=_('to'))

    #type = models.ForeignKey('RelationshipType')

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
    comment = ''

    def __init__(self, *args, **kwargs):
        super(Relation, self).__init__(*args, **kwargs)
        self.original = deepcopy(self)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = self.creator or self.user
            super(Relationship, self).save(*args, **kwargs)
            alteration = Alteration(fr=self.fr, be=self.be, to=self.to, of=self, by=self.creator, comment = self.comment, initial=True)
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
                alteration = Alteration(fr=self.fr, be=self.be, to=self.to, of=self, by=self.user, comment=self.comment)
                alteration.save()

            super(Relationship, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('relation', args=[self.pk])

    def get_update_url(self):
        return reverse('update-relation', args=[self.pk])


class Alteration(models.Model):
    """Any alteration of relationships."""
    fr = models.ForeignKey('Entry', related_name="source_entry", verbose_name=_('from'))
    be = models.ForeignKey('Entry', related_name="type_of", verbose_name=_('be'))
    to = models.ForeignKey('Entry', related_name="target_entry", verbose_name=_('to'))

    of = models.ForeignKey(Relation, related_name='relationship', verbose_name=_('of')) # what
    by = models.ForeignKey(User, related_name='person', verbose_name=_('by'))   # who
    at = models.DateTimeField(_('at'), auto_now=True)    # when
    initial = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, blank=True, null=True)

    previous_version = None

    def __unicode__(self):
        if self.initial:
            action = 'initialized'
        else:
            action = 'altered'
        return "{0} {1} {2} to {3} by {4} at {5}".format(self.fr, self.be, self.to, self.of, self.by, self.at,
                                                      action)

    def get_absolute_url(self):
        return reverse('detail-alteration', args=[self.pk])

    def previous(self):
        if self.previous_version:
            return self.previous_version
        try:
            self.previous_version = Alteration.objects.filter(Q(of=self.of) & Q(pk__lt=self.pk)).order_by('-pk')[0]
            return  self.previous_version
        except:
            return ''


class Category(models.Model):
    name = models.CharField(_('name'), max_length=255, unique=True)
    synonyms = models.ManyToManyField('self', blank=True, verbose_name=_('synonyms'))
    definition = models.ForeignKey('Entry', related_name=_('category'), blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail-category', args=[self.pk])

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    """A category tag modeling a namespace."""
    name = models.CharField(_('name'), max_length=255, unique=True)
    synonyms = models.ManyToManyField('self', blank=True, verbose_name=_('synonyms'))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('entry-tag', args=[self.name]) #u"/data/tag/%s" % self.pk


class EntryDummy(object):
    def __init__(self, title=None, text=None, tags=None, images=None, urls=None):
        self.title = title
        self.text = text
        self.tags = tags
        self.images = images
        self.urls = urls

    def content(self):
        return self.text or mark_safe('<a href="%s">o</a>' % self.generate())

    def generate(self):
        return reverse('generate-entry', args=[self.title])


# Signals:
#request_finished.connect(handlers.request_finished)
#pre_save.connect(handlers.saving_model, sender=Entry)
#post_save.connect(handlers.model_saved, sender=Entry)
#reversion.pre_revision_commit.connect(handlers.pre_revision, sender=Entry)
#reversion.post_revision_commit.connect(handlers.post_revision, sender=Entry)
m2m_changed.connect(handlers.changed_tags, sender=Entry.tags.through)
m2m_changed.connect(handlers.changed_tagged, sender=Entry.tagged.through)
m2m_changed.connect(handlers.changed_categories, sender=Entry.images.through)
m2m_changed.connect(handlers.changed_images, sender=Entry.images.through)
#message_sent.connect(handlers.message_sent)
signals.tags_added.connect(handlers.adding_tags)

#2345678911234567892123456789312345678941234567895123456789612345678961234567897123456789