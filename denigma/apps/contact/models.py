"""Illustrated recursive, symmetrical many-to-many relationships.
http://www.caktusgroup.com/blog/2009/08/14/creating-recursive-symmetrical-many-to-many-relationships-in-django/"""
from django.db import models


class Contact(models.Model):
    contacts = models.ManyToManyField(
        'self',
        through='ContactRelationship',
        symmterical=False,
        related_name='related_contacts+'
    )


class Relationship(models.Model):
    types = models.ManyToManyField(
        'RelationshipType',
        related_name='contact_relationships',
        blank=True,
    )
    from_contact = models.ForeignKey('Contact', related_name='from_contacts')
    to_contact = models.ForeignKey('Contact', related_name='to_contacts')

    class Meta:
        unique_together = ('from_contact', 'to_contact')


class RelationshipType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()