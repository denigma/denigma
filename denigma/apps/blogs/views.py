from django.shortcuts import render_to_response
from blogs.models import Blog


def index(request):
    entries = Blog.objects.all()
    return render_to_response('blogs/index.html', locals())
