from django.conf.urls.defaults import patterns
from django.views.generic.create_update import update_object, delete_object
from django.template import loader

import views
from models import Todo


urlpatterns = patterns('', # Pattern definition
    (r'^login$', views.todo_login),
    (r'^logout$', views.todo_logout),
                       
    (r'^$', views.todo_index),
    (r'^add$', views.add_todo),
    (r'^(\d+)$', views.view_todo),
    (r'^(?P<todo_id>\d+)/{0,1}$', views.update_todo),
    (r'^(?P<todo_id>\d+)/delete$', views.delete_todo),
    (r'^(\d+)/edit$', 'todos.views.edit_todo'),
)
