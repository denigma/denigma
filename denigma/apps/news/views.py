from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.shortcuts import render_to_response

from blog.models import Post


def index(request):
     news = Post.objects.filter(tags__name='news').order_by('-created', '-id')
     paginator = Paginator(news, 5)
     page_num = request.GET.get('page', 1)
     try:
         page = paginator.page(page_num)
     except EmptyPage:
         page = paginator.page(paginator.num_pages)
     except PageNotAnInteger:
         page = paginator.page(1)
     ctx = {'page': page}
     return render_to_response('news/index.html', ctx,
                               context_instance=RequestContext(request))

def year_archive(request, year):
    a_list = Article.objects.filter(pub_date__year=year)
    return render_to_response('news/year_archive.html', {'year': year, 'article_list': a_list})
