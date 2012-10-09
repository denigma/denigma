"""The data control module."""
from django.contrib.auth.models import User

try:
    from blog.models  import Post # To be replaced by data entry model
except Exception as e:
    print ("data.models: %s" % e)

from models import Entry, EntryDummy


def get(title, text=None, tags=None, images=None, urls=None):
    """Fetches an data entry according to its title."""
    try:
        entry = Entry.objects.get(title=title)
        #print("Got entry: %s" % entry)
    except (Entry.DoesNotExist):
        try:
            entry = Post.objects.get(title=title)
        except (Post.DoesNotExist, Post.MultipleObjectsReturned) as e:
            entry = EntryDummy(e)
        except (Entry.MultipleObjectsReturned) as e:
            entry = Entry.objects.filter(title=title)[0]
    return entry

def init(post=None):
    """Initialises a data entry from a blog post."""
    user = User.objects.get(username="Hevok")
    posts = Post.objects.all()
    if post:
        posts = [posts[post]]
    for index, post in enumerate(posts):
        try:
            #entry = Entry(**{'post':post, 'user':user})
            entry = Entry(post, user)
            entry.save()
        except Exception as e:
            print("data.models.init: %s (%s %s)" % (e, index, post.title))

