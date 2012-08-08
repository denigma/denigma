from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from shorty.models import *
from shorty.forms import *

def visit(request, key):
    key = ShortyURL.id_for_key(key)
    shorty = get_object_or_404(ShortyURL, pk=key)
    user_agent_string = request.META['HTTP_USER_AGENT']

    visit = Visit(shorty=shorty, user_agent_string=user_agent_string)
    visit.save()
    return redirect(shorty.source.url, permanent=True)

def home(request):
    if request.method == "POST":
        form = SourceForm(request.POST)
        if form.is_valid():
            source = form.save()
            return redirect('source', source.admin_key)
    else:
        form = SourceForm()

    return render_to_response('home.html', RequestContext(request, {'form' : form}))

def manage(request, admin_key):
    source = get_object_or_404(SourceURL, admin_key=admin_key)
    if request.method =="POST":
        pk = request.POST['id']
        shorty = source.shorty_urls.get(pk=pk)
        shorty.notify = not shorty.notify
        shorty.save()
    return render_to_response("manage_source.html", RequestContext(request, {'source' : source}))
