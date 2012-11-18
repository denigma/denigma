from django.conf.urls.defaults import patterns, url
from django.views.generic.create_update import update_object, delete_object
from django.template import loader
from django.views.generic import CreateView

from models import Todo
from views import TodoCreate


urlpatterns = patterns('todos.views', # Pattern definition
    url(r'^login$', 'todo_login'),
    url(r'^logout$', 'todo_logout'),
                       
    url(r'^$', 'todo_index', name='todos'),
    url(r'^add$', 'add_todo'),
    url(r'^create/$', TodoCreate.as_view(), name='create_todo'),

    url(r'^(\d+)/$', #views.view_todo),
    CreateView.as_view(
         model=Todo,
         template_name='todos/detail.html')
    ), # Depricacted?

    url(r'^(?P<todo_id>\d+)/{0,1}$', 'update_todo'),
    url(r'^(?P<todo_id>\d+)/delete$', 'delete_todo'),
    url(r'^(\d+)/edit$', 'edit_todo'),
)
