from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import AnonymousUser, User
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


import reversion

from models import Post
from forms import PostForm

from meta.view import log


class PostListView(ListView):
    model = Post # Implies -> queryset = models.Post.objects.all()
    template_name = 'blog/index.html'
    context_object_name = "object_list"
    paginate_by = 10


def add(request):
    form = PostForm(request.POST or None)
    if request.POST and form.is_valid():
        with reversion.create_revision():
            post = form.save(commit=False)
            form.save()
            if isinstance(request.user, AnonymousUser):
                request.user = User.objects.get(username="Anonymous")
            reversion.set_user(request.user)
            comment = request.POST['comment'] or "Initial version."
            reversion.set_comment(comment)
            log(request, post, comment)
            return redirect('/blog/')
            #return render_to_response('blog/index.html',
            #                          context_instance=RequestContext(request))
    return render_to_response('blog/add.html', {'form': form},
                              context_instance=RequestContext(request))

@login_required
def edit(request, pk):
    if request.method == 'GET':
        post = Post.objects.get(pk__exact=pk)
        form = PostForm(instance=post)
        Post.text = post.text
    elif request.method == 'POST':
        post = Post.objects.get(pk__exact=pk)

        # Tracking changes:
        changes = []
        if post.title != request.POST['title']:
            s1 = post.title
            s2 = request.POST['title']
            changes.append('title (%s)' % "".join(["-"]+s1.split(s2) if len(s1) > len(s2) else ["+"]+s2.split(s1)))
        if post.text != request.POST['text']:
            changes.append('text')
        if set([tag.name for tag in post.tags.all()]) != set(request.POST['tags'].split(', ')):
            changes.append('tags')
        if "images" in request.POST:
            dict = {}
            dict.update(request.POST)
            pre_images = set(dict['images'])
            post_images = set([unicode(image.pk) for image in post.images.all()])
            if pre_images != post_images:
                changes.append('images (%s)' %  "; ".join(pre_images - post_images))
        if "published" in request.POST:
            if not post.published:
                changes.append('published to True')
        elif post.published:
            changes.append('published to False')

        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            if changes:
                with reversion.create_revision():
                    form.save()
                    reversion.set_user(request.user)
                    comment =  'Changed %s.%s' % (' '+', '.join(changes),request.POST['comment'] or '')
                    reversion.set_comment(comment)

                log(request, post, comment)

            else:
                form.save()

            return HttpResponseRedirect('/blog/%s' % pk)
    return render_to_response('blog/edit.html', {'form': form},
                              context_instance=RequestContext(request))
    #return HttpResponse('edit post')


def tagpage(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    return render_to_response("blog/tagpage.html", {"posts": posts, "tag":tag},
        context_instance=RequestContext(request))



# Custom admin:
from django.contrib.auth.decorators import permission_required


@permission_required('blog.add_post')
def custom_admin_view(request, model_admin):
     opts = model_admin.model._meta
     admin_site = model_admin.admin_site
     has_perm = request.user.has_perm(opts.app_label + '.' \
                                      + opts.get_change_permission())
     context = {
         'admin_site': admin_site.name,
         'title': "My Custom View",
         'opts': opts,
         'root_path': '\%s' % admin_site.root_path,
         'app_label': opts.app_label,
         'had_change_permission': has_perm
     }
     template = 'admin/custom/view.html'
     return render_to_response(template, context,
                              context_instance=RequestContext(request))
