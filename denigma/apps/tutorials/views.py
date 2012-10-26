from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q

from data.models import Entry


def index(request):
    tutorials_entry = Entry.objects.get(title="Tutorials")
    tutorials = Entry.objects.filter(Q(tags__name='tutorial') | Q(categories__name="Tutorial")).order_by('id').distinct()
    ctx = {'tutorials_entry': tutorials_entry, 'tutorials': tutorials}
    return render_to_response('tutorials/index.html', ctx,
                              context_instance=RequestContext(request))

def view(request, tutorial_id):
    print "Tutorial id is:", tutorial_id, type(tutorial_id)
    tutorial = Entry.objects.get(pk=tutorial_id)
    return render_to_response("./tutorials/view.html", {'tutorial': tutorial},
                              context_instance=RequestContext(request, {}))

def edit(request, tutorial_id):
    tutorial = Entry.object.get(pk=tutorial_id)
    return render_to_response("./tutorials/view.html", {'tutorial': tutorial},
                             context_instance=RequestContext(request, {}))

def development(request):
    """Operation-specific developments considerations."""
    windows = Entry.objects.get(title="Windows")
    mac = Entry.objects.get(title="Mac")
    linux = Entry.objects.get(title="Linux")
    ctx = {'windows': windows, 'mac': mac, 'linux': linux}
    return render_to_response('tutorials/development.html', ctx,
                              context_instance=RequestContext(request))
#234567891123456789212345678931234567894123456789512345678961234567897123456789