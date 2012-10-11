from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from idios.models import ProfileBase

import aspects


class Profile(ProfileBase):
    """A user profile extending auth user."""
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)

    rank = models.ForeignKey('aspects.Rank', blank=True, null=True)
    #grade = models.ForeignKey('aspects.Grade', blank=True, null=True)
    grades = models.ManyToManyField('aspects.Grade', blank=True, null=True)
    title = models.ForeignKey('aspects.Title', blank=True, null=True)
    role = models.ManyToManyField('aspects.Role', blank=True, null=True)

    last_list_check = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('profile-detail', args=[self.name])

    def promote(self, aspect, level):
        """Executes a promotion."""
        promoted = False
        if aspect == 'rank' and not self.rank:
            self.rank = aspects.models.Rank.objects.all()[0] #get(pk=int(level))
            promoted = True
        elif aspect == 'grade' and not self.grades.all():
            self.grades.add(aspects.models.Grade.objects.all()[0]) #get(pk=int(level))
            promoted = True
        elif aspect == 'title' and not self.title:
            print aspects.models.Title.objects.all()[0]
            self.title = aspects.models.Title.objects.all()[0] #get(pk=int(level))
            promoted = True
        self.save()
        return promoted



class Rank(models.Model):
    """A scientific research rank in militarian convention."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    requirement = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Grade(models.Model):
    """A developer programming grade in marshal arts convention."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    symbol = models.ForeignKey('gallery.PhotoUrl', blank=True, null=True)
    requirement = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Title(models.Model): # Degree
    """An artistic designer degree in spirituell christian schema."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    symbol = models.ForeignKey('gallery.PhotoUrl', blank=True, null=True)
    requirement = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    """A special appointed role."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    symbol = models.ForeignKey('gallery.PhotoUrl', blank=True, null=True)

    def __unicode__(self):
        return self.name