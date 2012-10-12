# -*- coding: utf-8 -*-
"""Views for links."""
from django.views.generic import list_detail, ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.db.models import Q

from django_tables2 import SingleTableView

from data.models import Entry
from data.views import Create, Update

from models import Link
from tables import LinkTable
from forms import LinkForm, FilterForm


def links_by_language(request):
    # Use the object_list view for the heavy lifting:
    language = request.LANGUAGE_CODE
    print language
    return list_detail.object_list(
        request,
        queryset = Link.published.all(),#.filter(language=language),
        template_name = "links/links_by_language.html",
        template_object_name = "links",
        )


class LinkView(object):
    model = Link
    form_class = LinkForm
    template_name='/links/index.html'
    success_url = '/links/'


import django_filters


class Filter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['title', 'description']


class Links(SingleTableView, FormView, LinkView):
    table_class = LinkTable
    queryset = Link.objects.filter(site__domain='denigma.de')
    form_class = FilterForm
    success_url = '/links/'
    query = None
    template_name = 'links/index.html'

    def form_valid(self, form):
        Links.query = form.cleaned_data['filter']
        return super(Links, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(Links, self).get_context_data(*args, **kwargs)
        context['entry'] = Entry.objects.get(title='Links')
        context['form'] = FilterForm(initial={'filter': Links.query})
        return context

    def get_queryset(self):
        if Links.query:
            return Link.objects.filter(Q(title__icontains=Links.query) |
                                       Q(description__icontains=Links.query) #|
                                       #Q(category__title=Links.query)
                                      )
        else:
            return Link.objects.all()


class LinkList(ListView):
    queryset = Link.objects.filter(site__domain='denigma.de'),
    context_object_name ='links'


class LinkUpdate(LinkView, Update):
    pass
#

class LinkCreate(LinkView, Create):
    model = Link
    form_class = LinkForm
    def form_invalid(self, form):
        #print form
        print form.errors
        print "invalid form."
        print self.model
        return redirect('/links/')
