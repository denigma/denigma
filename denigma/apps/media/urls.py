from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns('media.views',
    url(r'^$', 'index', name='media'),
    url(r'^slides', TemplateView.as_view(template_name='gallery/slides.html'), name='slides'),
    url(r'^add/.+$', 'newImage'),
)