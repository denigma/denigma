from django.db import models
##from djangotoolbox.fields import ListField
##
##class Post(models.Model):
##    title = models.CharField()
##    text = models.TextField()
##    tags = ListField()
##    comments = ListField()

class Blog(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()


