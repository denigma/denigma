from django.conf.urls import url, patterns


urlpatterns = patterns('network.views',
    url(r'^$', 'gba', name='gba'),
)
