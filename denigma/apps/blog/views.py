from models import Post
from django.shortcuts import render_to_response


def tagpage(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    return render_to_response("blog/tagpage.html", {"posts": posts, "tag":tag})
