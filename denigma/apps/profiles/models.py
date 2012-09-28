from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase


class Profile(ProfileBase):
    """A user profile extending auth user."""
    name = models.CharField(_("name"), max_length=50, null=True, blank=True)
    about = models.TextField(_("about"), null=True, blank=True)
    location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)

    rank = models.ForeignKey('Rank', blank=True, null=True)
    grade = models.ForeignKey('Grade', blank=True, null=True)
    #grades = models.ManyToMany('Grade', blank=True, null=True)
    title = models.ForeignKey('Title', blank=True, null=True)
    role = models.ManyToManyField('Role', blank=True, null=True)

    def promote(self, aspect, level):
        """Executes a promotion."""
        ASPECTS = {1:'rank', 2:'grade', 3:'title', 4:'role'}
        aspect = ASPECTS[aspect]
        self.setattr(aspect, level)


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
    requirement = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Title(models.Model): # Degree
    """An artistic designer degree in spirituell christian schema."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    requirement = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Role(models.Model):
    """A special appointed role."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

#class Abstract(models.Model):
#    name = models.CharField(max_length=255, unique=True)
#    description = models.TextField(blank=True, null=True)
#    symbol = models.ForeignKey('gallery.PhotoUrl')
#    requirement = models.CharField(max_length=255, blank=True, null=True)
#    class Meta:
#        abstract = True
#    def __unicode__(self):
#        return self.name
#
#
#class Hierarchy(Abstract):
#    type = models.ForeignKey('HierarchyType', blank=True)
#
#
#class HierarchyType(Abstract):
#    """Rank, Grade, Title, etc."""
#
#class Rank(Hierarchy):
#    """A scientific research rank in military convention."""
#
#
#class Grade(Hierarchy):
#    """A developer programming grade in marshal arts convention."""
#    language = models.ForeignKey('Language')
#
#
#class Title(Hierarchy): # Degree
#    """An artistic designer degree in spiritual christian schema."""
#
#
#class Language(Abstract):
#    """A programming language."""
#
#
#class Role(Hierarchy):
#    """A special appointed role."""

