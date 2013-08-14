from django.db import models
from django.contrib.sessions.models import Session
#from django.contrib.auth.models import User


class Task(models.Model):
    session = models.ForeignKey(Session)
    label = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    #user = models.ForeignKeyField(User) #/creator

    def __unicode__(self):
        return self.label
