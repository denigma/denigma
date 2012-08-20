from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    
    def __unicode__(self):
        return self.name
