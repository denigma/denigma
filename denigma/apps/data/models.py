from django.db import models


class EntryDummy(object):
    def __init__(self, title=None, text=None, tags=None, images=None, urls=None):
        self.title = title
        self.text = text
        self.tags = tags
        self.images = images
        self.urls = urls
