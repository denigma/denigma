# -*- coding: utf-8 -*-
"""Views for links."""
from django.views.generic import list_detail, ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.db.models import Q

from django_tables2 import SingleTableView

import django_filters

from data import get
from data.models import Entry
from data.views import Create, Update

from add.forms import handlePopAdd

from models import Link, Category
from tables import LinkTable
from forms import LinkForm, CategoryForm, CountryForm, FilterForm
from filters import LinkFilterSet


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
    category = None

    def form_valid(self, form):
        Links.query = form.cleaned_data['filter']
        return super(Links, self).form_valid(form)

    def form_invalid(self, form):
        Links.query = None
        return super(Links, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        #print("links.Links.dispatch")
        if 'category' in kwargs:
            self.category = kwargs['category']
        else:
            self.category = ''
        return super(Links, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Links, self).get_context_data(**kwargs)
        context['entry'] = get("Links")
        context['form'] = FilterForm(initial={'filter': Links.query})
        context['filterset'] = self.filterset
        context['categories'] = Category.objects.all()
        if self.category:
            context['category'] = Category.objects.get(slug=self.category)
        else:
            context['category'] = None
        return context

    def get_queryset(self):
        #print("links.Links.get_queryset: %s" % self.category)
        qs = self.queryset.order_by('title')
        if self.category:
            qs = qs.filter(category__slug__exact=self.category)
        if Links.query:
            terms = Links.query.split(None)
            for term in terms:
                qs = qs.filter(Q(title__icontains=term) |
                               Q(description__icontains=term) |
                               Q(url__icontains=term)
                )
        self.filterset = LinkFilterSet(qs, self.request.GET)
        return self.filterset.qs


class LinkList(ListView):
    queryset = Link.objects.filter(site__domain='denigma.de'),
    context_object_name ='links'


class LinkUpdate(LinkView, Update):
    pass


class LinkCreate(LinkView, Create):
    model = Link
    form_class = LinkForm
    def form_invalid(self, form):
        #print form
        #print form.errors
        #print "invalid form."
        #print self.model
        return redirect('/links/')


class CategoryCreate(Create):
    model = Category
    form_class = CategoryForm


class CategoryUpdate(Update):
    model = Category
    form_class = CategoryForm


def newCategory(request):
    return handlePopAdd(request, CategoryForm, 'category')

def newCountry(request):
    return handlePopAdd(request, CountryForm, 'countries')