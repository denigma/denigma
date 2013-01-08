from django.db import models


class ResearchManager(models.Manager):
    def get_query_set(self):
        return super(ResearchManager, self).get_query_set().filter(category__title__startswith="r")

