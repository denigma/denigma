from django.conf.urls import patterns, url

from django.views.generic import TemplateView

from models import Image
from views import ImageView


urlpatterns = patterns('media.views',
    url(r'^$', 'index', name='media'),
    url(r'^slides', TemplateView.as_view(template_name='gallery/slides.html'), name='slides'),
    url(r'^(?P<pk>\d+)', ImageView.as_view(), name='detail-image')
    #url()
)