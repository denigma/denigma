from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20, primary_key=True)


class Page(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    
