"""Illustrates how to define a through table:
http://stackoverflow.com/questions/2854350/django-admin-many-to-many-listbox-doesnt-show-up-with-a-through-parameter
"""
from django.db import models
from django.contrib.auth.models import User
from somewhere import tags # figure out which is the best option


class Message(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User)
    thread = models.ForeignKey('self', blank=True, null=True)


class Forum(models.Model):
    name = models.CharField(max_length=24)
    messages = models.ManyToManyField(Message, through="Message_forum",
                                      blank=True, null=True)



class Message_forum(models.Model):
    message = models.ForeignKey(Message)
    forum = models.ForeignKey(Forum)
    status = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)



