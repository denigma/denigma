from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('news.views',
    url('^$', 'index', name='news'),
    url('^(\d{4})/$', 'year_archive'),
   # url(r'^(\d{4})/(\d{2})/$', 'month_archive'),
   # url(r'^(\d{4})/(\d{2})/(\d+)/$', 'article_detail'),
)
