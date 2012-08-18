from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from models import PastedItem


info_dict = {
    'queryset': PastedItem.objects.all(),
    'slug_field': 'uuid',
}

urlpatterns = patterns('',
    url(r'^pre/$', # Previous (depricated).
        direct_to_template,
        {"template": "pastebin/pre.html"},
        name="pastebin"),
   url(r'^$', 'pastebin.views.new', name='pastebin_new'),
   url(r'^(?P<slug>[-0-9a-f]{36})/$',
       'django.views.generic.list_detail.object_detail',
       info_dict,
       'pastebin_detail'),
)
