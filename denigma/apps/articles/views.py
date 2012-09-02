from django.shortcuts import render_to_response

from blog.models import Post


def view(request, title):
    """Viewing article by title."""
    post = Post.objects.get(title=title)
    return render_to_response('articles/view.html', {'post': post})
