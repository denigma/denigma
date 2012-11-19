from django.conf.urls import patterns, url
from django.views import generic

urlpatterns = patterns('',
    url(r'^about$', generic.TemplateView.as_view(
        template_name='about.html'),
        name='about-page'
    )
)