import datetime

from django.db import models
from django.contrib.auth.models import User


# Constrain choices
importance_choices = (
    ('A', 'Very Important'),
    ('B', 'Important'),
    ('C', 'Medium'),
    ('D', 'Unimportant'),
)

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    importance = models.CharField(max_length=1, choices=importance_choices)
    start_date = models.DateField(blank=True, null=True)
    stop_date = models.DateField(blank=True, null=True)
    created = models.DateField(auto_now_add=True) # 'creation date'
    updated = models.DateField(auto_now=True)
    #finished = models.DateField(blank=True, null=True)
    done = models.BooleanField()
    owner = models.ForeignKey(User, blank=True)
    #deadlines?
    # email to inform people before deadlines end.

    def was_created_today(self):
        return self.date.date() == datetime.date.today()
    was_created_today.short_description = 'Created today?'

    def text_importance(self):
        choices = dict(importance_choices)
        return choices[self.importance]

    def short_description(self):
        return self.description.split('\n')[0][:80] + '...'

    def __unicode__(self):
        return self.title
    
