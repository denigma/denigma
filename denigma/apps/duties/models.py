from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


#priorities = (
#    (0, 'Very high'),
#    (1, 'High'),
#    (2, 'Medium'),
#    (3, 'Low'),
#)
#
#
#class Duty(models.Model):
#    """Used if no Task or Todo is present."""
#    name = models.CharField(max_length=250, verbose_name=_("Title"))
#    description = models.TextField(blank=True, null=True)
#    priority = models.IntegerField(choices=priorities) # Importance
#    difficulty = models.IntegerField(default=0)
#
#    created = models.DateTimeField(auto_now_add=True)
#    updated = models.DateTimeField(auto_now=True)
#
#    start = models.DateTimeField(blank=True, null=True)
#    stop = models.DateTimeField(blank=True, null=True)
#
#    done = models.BooleanField(default=False)  # status
#    onhold = models.BooleanField(default=False)
#    progress = models.IntegerField(default=0)
#
#    #project = models.ForeignKey('Project', blank=True, null=True)
#
#    creator = models.ForeignKey(User, related_name='Nominator')
#    executors = models.ManyToManyField(User, blank=True, null=True, related_name='Executors')
#
#    def __unicode__(self):
#        return self.name
#
#    class Meta:
#        verbose_name_plural = _("Duties")
#
#
##class Project(models.Model):
##    name = models.CharField(max_length=100)
##    creator = models.ForeignKey(User)
##
##    def __unicode__(self):
##        return self.name
#
#
#class Objective(models.Model):
#    content_type = models.ForeignKey(
#        ContentType,
#        verbose_name=_('Content_type'),
#        related_name="%(app_label)s_%(class)s_tagged_items")
#    content_object = GenericForeignKey()
#
#    duty = models.ForeignKey(Duty)
#
#    def __unicode__(self):
#        return u"%s: %s" % (self.duty, self.content_object)
