from django.db import models


class Abstract(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    symbol = models.ForeignKey('gallery.PhotoUrl', blank=True, null=True)
    requirement = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.name


class Hierarchy(Abstract):
    type = models.ForeignKey('HierarchyType', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Hierarchies'


class HierarchyType(Abstract):
    """Rank, Grade, Title, etc."""
    pass


class Rank(Hierarchy):
    """A scientific research rank in military convention."""


class Grade(Hierarchy):
    """A developer programming grade in marshal arts convention."""
    language = models.ForeignKey('Language', blank=True, null=True)


class Title(Hierarchy): # Degree
    """An artistic designer title in spiritual christian schema."""


class Role(Hierarchy):
    """A special appointed role."""


class Language(Abstract):
    """A programming language."""

