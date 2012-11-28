import datetime

from django.db import models
from django.contrib.auth.models import User


# Constrain choices
priorities = (
    ('A', 'Very high'),
    ('B', 'High'),
    ('C', 'Medium'),
    ('D', 'Low'),
)

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    importance = models.CharField(max_length=1, choices=priorities, verbose_name='priority')
    created = models.DateField(auto_now_add=True) # 'creation date'
    updated = models.DateField(auto_now=True)
    start_date = models.DateField(blank=True, null=True)
    stop_date = models.DateField(blank=True, null=True)
    #finished = models.DateField(blank=True, null=True)
    done = models.BooleanField()
    owner = models.ForeignKey(User, blank=True)
    #deadlines?
    # email to inform people before deadlines end.

    quest = 'conversion'

    def was_created_today(self):
        return self.date.date() == datetime.date.today()
    was_created_today.short_description = 'Created today?'

    def text_importance(self):
        choices = dict(priorities)
        return choices[self.importance]

    def short_description(self):
        return self.description.split('\n')[0][:80] + '...'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return u"/todos/%s" % self.pk
    
