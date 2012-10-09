from django.db import models


class EntryManager(models.Manager):
    def published_entries(self):
        return self.model.objects.filter(published=True)
