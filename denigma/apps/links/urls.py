# -*- coding: utf-8 -*-
"""Urls for links."""
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import  Links, LinkList, LinkUpdate, LinkCreate #links_by_language
from views import  CategoryCreate, CategoryUpdate


urlpatterns = patterns('',
    url(r'^$', Links.as_view(), name='links'),
    url(r'list^$', LinkList.as_view(), name='link-list'), # Depricated
    #url(r'^language/$', links_by_language, name='links_list'), # Depricated
    url(r'^update/(?P<pk>\d+)', login_required(LinkUpdate.as_view()),
        name='update-link'),
    url(r'^create/$', LinkCreate.as_view(), name='create-link'),
    url(r'^category/create/$', CategoryCreate.as_view(), name='create-link-category'),
    url(r'^category/update/(?P<slug>.+)/$', login_required(CategoryUpdate.as_view()),
        name='update-link-category'),
    url(r'^category/(?P<category>.+)/$', Links.as_view(), name='links-category'),
)

