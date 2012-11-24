from django.conf.urls import patterns, url


urlpatterns = patterns("tasks.views",
    url(r'^$', 'index', name='tasks'),
    url(r'^(?P<pk>\d+)/done/$', 'mark_done', name='task_mark_done'),
    url(r'^(?P<pk>\d+)/undone/$', 'mark_undone', name='task_mark_undone'),
    url(r'^completed/$', 'complete_count_fragment', name='task_complete_count_fragment'),
    url(r'^add/$', 'add', name='task_add'),
    url(r'(?P<pk>\d+)/delete/$', 'delete', name='task_delete')
)

