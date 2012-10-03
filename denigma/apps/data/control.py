"""The data control module."""
from blog.models import Post # To be replaced by data entry model

from models import EntryDummy


def get(title, text=None, tags=None, images=None, urls=None):
    """Fetches a database entry according to its title."""
    try:
        entry = Post.objects.get(title=title)
    except (Post.DoesNotExist, Post.MultipleObjectsReturned) as e:
        entry = EntryDummy(e)
    return entry