"""Todos will be renamed to Duties."""
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

# Constrain choices
priorities = (
    ('A', 'Very high'),
    ('B', 'High'),
    ('C', 'Medium'),
    ('D', 'Low'),
)


class Todo(models.Model): # Rename To Duty
    title = models.CharField(max_length=200, help_text="The name of the todo")
    description = models.TextField(help_text="Informal description what the todo is about. Provide here useful links for instance")

    priority = models.CharField(max_length=1, choices=priorities, default='C', verbose_name='priority', help_text="The importance of a todo.") # Rename to priority.
    difficulty = models.IntegerField(default=0, help_text="The estimated difficulty to complete the todo (Give it a value from 1 to 10 where 10 is most difficult).")
    progress = models.IntegerField(default=0, help_text="The progress of the task in Percentage.")
    value = models.IntegerField(default=1, help_text="The <a href='Data Credit'>Data Credit</a> value that should be given to the executor on successful completion.")

    created = models.DateField(auto_now_add=True) # 'creation date'
    updated = models.DateField(auto_now=True)
    start_date = models.DateField(blank=True, null=True, help_text="Optional")
    stop_date = models.DateField(blank=True, null=True, help_text="Optional")
    #finished = models.DateField(blank=True, null=True)
    creator = models.ForeignKey(User, related_name='todos', blank=True, verbose_name=_("Creator")) # Rename to creator.
    executor = models.ManyToManyField(User, related_name='assigned_todos', blank=True, null=True, verbose_name=_("Executors"), help_text="The assigned user who should execute the todo (Optional).") #
    categories = models.ManyToManyField('data.Entry', related_name='todo', blank=True, null=True, help_text="The categories which this todo belongs to. It also be used to assign arbitrary kind of labels")
    done = models.BooleanField(help_text="Check this if the todo is successfully completed.")
    onhold = models.BooleanField(default=False, help_text="Check this if the todo was put on hold.")


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
        return reverse('detail-todo', args=[self.pk])
        #return u"/todos/%s" % self.pk
