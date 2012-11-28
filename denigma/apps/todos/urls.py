from django.conf.urls import patterns, url
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required

from models import Todo
from views import TodoCreate, TodoList


urlpatterns = patterns('todos.views', # Pattern definition
    url(r'^login$', 'todo_login'),
    url(r'^logout$', 'todo_logout'),
                       
    url(r'^$', 'todo_index', name='todo-list'),
    url(r'index/$', login_required(TodoList.as_view()), name='todos'),
    url(r'^add$', 'add_todo'),
    url(r'^create/(?P<task>.*)', TodoCreate.as_view(), name='create_todo'),
    url(r'^(\d+)/$', #views.view_todo),
    CreateView.as_view(
         model=Todo,
         template_name='todos/detail.html')
    ), # Deprecated?

    url(r'^(?P<todo_id>\d+)/{0,1}$', 'update_todo'),
    url(r'^(?P<todo_id>\d+)/delete$', 'delete_todo'),
    url(r'^(\d+)/edit$', 'edit_todo'),
)
