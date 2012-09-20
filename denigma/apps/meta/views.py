from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry


def index(request):
    users = User.objects.all()
    #logs = LogEntry.objects.all()
    ctx = {'users': users} #, 'logs': logs}
    return render_to_response('meta/index.html', ctx,
        context_instance=RequestContext(request))

def activity(request, pk):
    u = User.objects.get(pk=pk)
    logs = LogEntry.objects.filter(user=pk).order_by('-id')
    paginator = Paginator(logs, 10)
    page_num = request.GET.get('page', 1)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page = paginator.page(1)
    ctx = {'u': u, 'page': page}
    return render_to_response('meta/activity.html', ctx,
        context_instance=RequestContext(request))

def data(request):
    return render_to_response('meta/data.html', {'values':sorted(request.META.items())},
        context_instance=RequestContext(request))

def display(request):
    """Not used (depricated)."""
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))