from django.conf.urls.defaults import patterns
from django.views.generic.create_update import update_object, delete_object
from django.template import loader
from django.views.generic import CreateView

import views
from models import Todo


urlpatterns = patterns('todos.views', # Pattern definition
    (r'^login$', 'todo_login'),
    (r'^logout$', 'todo_logout'),
                       
    (r'^$', 'todo_index'),
    (r'^add$', 'add_todo'),

    (r'^(\d+)/$', #views.view_todo),
    CreateView.as_view(
         model=Todo,
         template_name='todos/detail.html')
    ), # Depricacted?

    (r'^(?P<todo_id>\d+)/{0,1}$', 'update_todo'),
    (r'^(?P<todo_id>\d+)/delete$', 'delete_todo'),
    (r'^(\d+)/edit$', 'edit_todo'),
)
