from django.http import HttpResponse
from django.shortcuts import render_to_response, render
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


#from reversion.helpers import generate_patch, generate_patch_html
from helpers import generate_patch, generate_patch_html
from reversion.admin import Version
from blog.models import Post


def diff(request, pk):
    print pk
    post = Post.objects.all()[int(pk)]
    available_versions = Version.objects.get_for_object(post)
    revisions = []
    for i in xrange(len(available_versions)-1):
        old_version = available_versions[i]
        print vars(old_version)
        new_version = available_versions[i+1]
        #patch = generate_patch(old_version, new_version, "text")
        patch_html = generate_patch_html(old_version, new_version, "text")
        revisions.append(patch_html)
    return HttpResponse("<hr>".join(revisions))

def difference(request):
    post = Post.objects.all()[50]
    available_versions = Version.objects.get_for_object(post)
    old_version = available_versions[0]
    new_version = available_versions[1]
    patch = generate_patch(old_version, new_version, "text")
    patch_html = generate_patch_html(old_version, new_version, "text")
    return HttpResponse(patch_html)

def links(request, template='meta/links.html'):
    """Retrieves all related links of an user."""
    user = User.objects.get(username=request.user)
    related_links = [rel.get_accessor_name() for rel in
                     user._meta.get_all_related_objects()]
    return render(request, template, {'related_links': related_links})

def objects(request, link=None, template='meta/objects.html'):
    """Retrieves and lists all objects related to an user."""
    user = User.objects.get(username=request.user)
    related_links = [rel.get_accessor_name() for rel in
                     user._meta.get_all_related_objects()]
    object_list = []
    for related_link in related_links:
        objects = getattr(user, related_link).all()
        if related_link == link:
            for object in objects:
                object_list.append(object)
    ctx = {'link': link,
           'objects': object_list}
    return render(request, template, ctx)




