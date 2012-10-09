from django.dispatch import Signal


tags_added = Signal(providing_args=['tags', 'instance'])