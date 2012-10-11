"""The data control module."""
from django.contrib.auth.models import User

try:
    from blog.models  import Post # To be replaced by data entry model
except Exception as e:
    print ("data.models: %s" % e)

from models import Entry, EntryDummy


def get(*args, **kwargs): #title=None, text=None, tags=None, images=None, urls=None
    """Fetches an data entry according to its title."""
    data = []
    #print len(args), args
    for title in args:
        try:
            entry = Entry.objects.get(title=title)
            data.append(entry)
            #print("Got entry: %s" % entry)
        except (Entry.DoesNotExist):
            try:
                post = Post.objects.get(title=title)
                data.append(post)
            except (Post.DoesNotExist, Post.MultipleObjectsReturned) as e:
                dummy = EntryDummy(title=title, text=e)
                data.append(dummy)
            except (Entry.MultipleObjectsReturned) as e:
                entry = Entry.objects.filter(title=title)[0]
                data.append(entry)
    if len(args) == 1: return data[0]
    elif len(args) > 1: return data


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

def execute():
    from models import Change
    from datetime import datetime
    changes = Change.objects.filter(at__lt=datetime(2012,10,10))
    changes.update(initial=True)
    print len(changes)
    return changes