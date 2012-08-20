import datetime

#from django.utils import timezone # Not avilable in Django 1.3.
from django.db import models


class Poll(models.Model): #  Inherit from models class.
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question
    
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'

    def was_published_recently(self): # Note: not available with Django 1.3.
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7) # A week.
    

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
    def __unicode__(self):
        return self.choice



    
