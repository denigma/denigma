from django.conf.urls import url, patterns

from data.views import EntryView


urlpatterns = patterns('quests.views',
    url(r'^$', 'index', name="quests"),
    url(r'^quest/(?P<slug>.+)', EntryView.as_view(
        template_name='quests/view.html',
        context_object_name='quest'), name="quest")
)