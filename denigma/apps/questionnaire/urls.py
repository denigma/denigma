from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import Questionnaires, ViewQuestionnaire, UserQuest, UserQuests, QuestStates


urlpatterns = patterns('questionnaire.views',
    url(r'^$', Questionnaires.as_view(), {}, "questionnaires"),
    url(r'^/questionnaire/(?P<dpk>\d+)/(?P<section>\d+)/$',
        ViewQuestionnaire.as_view(), {}, "questionnaire"),
    url(r'^/questionnaire/(?P<dpk>\d+)/$',
        ViewQuestionnaire.as_view(), {}, "questionnaire"),
    url(r'^/user-questionnaires/(?P<dpk>\d+)/$',
        UserQuests.as_view(), {}, "user_questionnaires"),
    url(r'^/user_questionnaire/(?P<dpk>\d+)/$',
        UserQuest.as_view(), {}, "user_questionnaire"),
    url(r'^/quest-stats/(?P<dpk>\d+)/$',
        QuestStates.as_view(), {}, "quest_stats"),
)

urlpatterns += patterns("django.views.generic",
    (r"^/done/$", "simple.direct_to_template", dict(template="questionnaire/done.html"), "done")
)