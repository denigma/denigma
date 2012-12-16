from datetime import datetime, timedelta
from django.db import models

from track import utils


class VisitorManager(models.Manager):
    def active(self, timeout=None, registered_only=True):
        #visitors = self.get_query_set().filter(expiry_time__gt=datetime.now(), end_time=None)
        if not timeout:
            timeout = utils.get_timeout()

        now = datetime.now()
        cutoff = now - timedelta(minutes=timeout)

        return  self.get_query_set().filter(last_update__gte=cutoff) #visitors #

    def registered(self):
        return self.get_query_set().filter(user__isnull=False)

    def guests(self):
        return self.get_query_set().filter(user__isnull=True)

