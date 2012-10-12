from django.db import models


class Abstract(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    symbol = models.ForeignKey('media.PhotoUrl', blank=True, null=True)
    requirement = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class Hierarchy(Abstract):
    type = models.ForeignKey('HierarchyType', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Hierarchies'

    def get_absolute_url(self):
        return u"/aspects/%s/%s" % (self.type.lower(), self.name.lower())


class HierarchyType(Abstract):
    """Rank, Grade, Title, etc."""
    profession = models.CharField(max_length=25, blank=True, null=True)
    aspect = models.CharField(max_length=25, blank=True, null=True)
    def get_absolute_url(self):
        return u"/aspects/achievement/%s" % (self.name.lower())


class Rank(Hierarchy):
    """A scientific research rank in military convention."""

    def get_absolute_url(self):
        return u"/aspects/research/rank/%s" % self.name.lower()


class Grade(Hierarchy):
    """A developer programming grade in marshal arts convention."""
    language = models.ForeignKey('Language', blank=True, null=True)

    def get_absolute_url(self):
        return u"/aspects/research/grade/%s" % self.name.lower()


class Title(Hierarchy): # Degree
    """An artistic designer title in spiritual christian schema."""

    def get_absolute_url(self):
        return u"/aspects/design/title/%s" % self.name.lower()


class Role(Hierarchy):
    """A special appointed role."""

    def get_absolute_url(self):
        return u"/aspects/role/%s" % self.name.lower()


class Language(Abstract):
    """A programming language."""

