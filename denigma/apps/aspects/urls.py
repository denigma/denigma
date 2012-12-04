from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import (AchievementCreate, HierarchyCreate,
                   RankCreate, GradeCreate, TitleCreate,
                   RankUpdate, GradeUpdate, TitleUpdate)


urlpatterns = patterns('aspects.views',
    # Professions:
    url(r'^$', 'index', name='aspects'),
    url(r'^professions/$', 'professions',name='professions'),
    url(r'^profession/(?P<name>\w+)', 'profession', name='profession'),

    # Achievements:
    url(r'^achievements/$', 'achievements', name='achievements'),
    url(r'^achievement/create/$',
        AchievementCreate.as_view(),
        name='create_achievement'),

    url(r'^ranks/create', RankCreate.as_view(), {'name': 'ranks'},
        name='create_rank'),
    url(r'^grades/create', GradeCreate.as_view(), {'name': 'grades'},
        name='create_grade'),
    url(r'^titles/create', TitleCreate.as_view(), {'name': 'titles'},
        name='create_title'),

    url(r'^rank/update/(?P<pk>\d+)', login_required(RankUpdate.as_view()),
        {'name': 'ranks'},
        name='update-rank'),
    url(r'^grade/update/(?P<pk>\d+)', login_required(GradeUpdate.as_view()),
        {'name': 'grades'},
        name='update-grade'),
    url(r'^title/update/(?P<pk>\d+)', login_required(TitleUpdate.as_view()),
        {'name': 'titles'},
        name='update-title'),

    url(r'^(?P<name>\w+)/create', HierarchyCreate.as_view(),
        name='create_hierarchy'),

    url(r'^achievement/add', 'add_achievement', name='add_achievement'),
    url(r'^(?P<aspect>\w+)/$', 'aspect', name='aspect'),
    url(r'^research/$', 'research', name='research'),
    url(r'^research/ranks/$', 'ranks', name='ranks'),
    url(r'^research/rank/(?P<name>\w+)', 'rank', name='rank'),
    url(r'^programming/$', 'programming', name='programming'),
    url(r'^programming/grades/$', 'grades', name='grades'),
    url(r'^programming/grade/(?P<name>[\w\s]+)', 'grade', name='grade'),
    url(r'^design/$', 'design', name='design'),
    url(r'^design/titles/$', 'titles', name='titles'),
    url(r'^design/title/(?P<name>\w+)', 'title', name='title'),
)
#234567891123456789212345678931234567894123456789512345678961234567897123456789