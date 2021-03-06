from django.db import models
from django.core.urlresolvers import reverse

class Entity(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ontology-entity-detail', args=[self.pk])

    @property
    def color(self):
        return self.text.split('\n')[0]

    class Meta:
        verbose_name_plural = 'Entities'


class Relation(models.Model):
    source = models.ForeignKey(Entity, related_name='target_relations')
    type = models.ForeignKey(Entity, related_name='relations')
    target = models.ForeignKey(Entity, related_name='source_relations')

    def __unicode__(self):
        return u"%s -%s-> %s " % (self.source, self.type, self.target)

    def get_absolute_url(self):
        return reverse('ontology-relation-detail', args=[self.pk])