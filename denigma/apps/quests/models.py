"""Questions and anserwers for Quests."""
from djanog.db import models


class Question(models.Model):
    title = models.CharField(max_length=250)
    text = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=125)
    is_correct = models.BooleanField()
    explanation = models.TextField(blank=True)
    added = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.text

    def is_crrect(self):
        return self.is_correct


# Create your models here.
