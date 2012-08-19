from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from models import PastedItem


info_dict = { # Obsolete?
    'queryset': PastedItem.objects.all(),
    'slug_field': 'uuid',
}

urlpatterns = patterns('',
    url(r'^pre/$', # Previous version (depricated).
        direct_to_template,
        {"template": "pastebin/pre.html"},
        name="pastebin"),
                       
   url(r'^$', 'pastebin.views.new', name='pastebin_new'),
                       
   url(r'^(?P<uuid>[-0-9a-f]{36})/$',
       'pastebin.views.detail',
       name='pastebin_detail'),

   url(r'^(?P<slug>[-0-9a-f]{36})/$', # Obsolete?
       'django.views.generic.list_detail.object_detail',
       info_dict,
       'pastebin_detail'),
)
