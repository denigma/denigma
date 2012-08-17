from django.db import models
##from djangotoolbox.fields import ListField
##
##class Post(models.Model):
##    title = models.CharField(max_lenth=100)
##    text = models.TextField()
##    tags = ListField()
##    comments = ListField()
##      created = models.DateTimeField(auto_now_add=True)
##      updated = models.DateTomeField(auto_now=True)
  

class Blog(models.Model):
    title = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __unicode__(self):
       return self.title

