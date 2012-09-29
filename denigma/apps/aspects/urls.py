from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('aspects.views',
    url(r'^$', 'index', name='aspects'),
    url(r'^professions/$', 'professions',name='professions'),
    url(r'^profession/(?P<name>\w+)', 'profession', name='profession'),
    url(r'^achievements/$', 'achievements', name='achievements'),
    url(r'^(?P<aspect>\w+)/$', 'aspect', name='aspect'),
    url(r'^research/$', 'research', name='research'),
    url(r'^research/ranks/$', 'ranks', name='ranks'),
    url(r'^research/rank/(?P<name>\w+)', 'rank'),
    url(r'^programming/$', 'programming', name='programming'),
    url(r'^programming/grades/$', 'grades', name='grades'),
    url(r'^programming/grade/(?P<name>[\w\s]+)', 'grade'),
    url(r'^design/$', 'design', name='design'),
    url(r'^design/titles/$', 'titles', name='titles'),
    url(r'^design/title/(?P<name>\w+)', 'title'),

)