from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Post


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
