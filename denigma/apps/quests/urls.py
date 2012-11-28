from django.conf.urls import url, patterns

from data.views import EntryView

from views import CreateQuest, EngageQuest


urlpatterns = patterns('quests.views',
    url(r'^$', 'index', name="quests"),
    url(r'^quest/(?P<slug>.+)', EntryView.as_view(
        template_name='quests/view.html',
        context_object_name='quest'), name="quest"),
    url(r'^engage/(?P<slug>.+)', EngageQuest.as_view(), name='engage-quest'),
    url(r'^todo/(?P<pk>\d+)', CreateQuest.as_view(), name='create-quest'),
)