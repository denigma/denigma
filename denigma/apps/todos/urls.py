from django.conf.urls import patterns, url
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required

from models import Todo
from views import TodoCreate, TodoList
from forms import TodoForm


urlpatterns = patterns('todos.views', # Pattern definition
    url(r'^login$', 'todo_login'),
    url(r'^logout$', 'todo_logout'),
                       
    url(r'^$', 'todo_index', name='todo-list'),
    url(r'index/$', login_required(TodoList.as_view()), name='todos'),
    url(r'^add$', 'add_todo'),
    url(r'^create/(?P<task>.*)', TodoCreate.as_view(), name='create_todo'),
    url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Todo, template_name='todo_detail.html'), name='detail-todo'),#views.view_todo),


    url(r'^(\d+)/$',
    CreateView.as_view(
         model=Todo,
         template_name='todos/detail.html')
    ), # Deprecated?

    url(r'^update/(?P<pk>\d+)/{0,1}$',
        UpdateView.as_view(model=Todo,
                           form_class=TodoForm),
        name='update_todo'),



    url(r'^(?P<todo_id>\d+)/delete$', 'delete_todo'),
    url(r'^(\d+)/edit$', UpdateView.as_view(model=Todo, form_class=TodoForm), name='update-todo'),
)
