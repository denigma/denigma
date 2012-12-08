"""Tutorials uses data entries in order to teach everything
to know in order to effectively alter Denigma."""
from django.shortcuts import render
from django.db.models import Q

from data import get
from data.models import Entry


def index(request, template='tutorials/index.html'):
    """generates a hierarchical list of all available tutorials."""
    tutorials_entry = get("Tutorials")
    tutorials = Entry.objects.filter(Q(tags__name='tutorial') |
                                     Q(categories__name="Tutorial"))\
                                    .order_by('id').distinct()
    ctx = {'tutorials_entry': tutorials_entry, 'tutorials': tutorials}
    return render(request, template, ctx)

def view(request, pk, template="./tutorials/view.html"):
    """Enables a detailed view on a tutorial."""
    #print("Tutorial id is:", tutorial_id, type(tutorial_id))
    tutorial = Entry.objects.get(pk=pk)
    return render(request, template, {'tutorial': tutorial})

def edit(request, pk, template="./tutorials/view.html"):
    """Allows to edit a data entry tutorial."""
    tutorial = Entry.object.get(pk=pk)
    return render(request, template, {'tutorial': tutorial})

def development(request, template='tutorials/development.html'):
    """Operation-specific developments considerations."""
    windows = get("Windows")
    mac = get("Mac")
    linux = get("Linux")
    ctx = {'windows': windows, 'mac': mac, 'linux': linux}
    return render(request, template, ctx)

#234567891123456789212345678931234567894123456789512345678961234567897123456789