from django.forms import Form, CharField
from django.db.models import Q
from django.views.generic.edit import FormView

from django_tables2 import SingleTableView

from django_easyfilters import FilterSet

from models import Entry


class FilterForm(Form):
    filter = CharField()


class EntryFilterSet(FilterSet):
    fields = ('categories', 'creator', 'created', 'updated')


class TableFilter(SingleTableView, FormView):
    form_class = FilterForm
    query = None
    filterset = None
    queryset = Entry.objects.filter(published=True).order_by('-created')
    success_url = '/data/entry/table/'
    # Guess success_url: app_name/index

    def form_valid(self, form):
        TableFilter.query = form.cleaned_data['filter']
        return super(TableFilter, self).form_valid(form)

    def form_invalid(self, form):
        TableFilter.query = None
        return super(TableFilter, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TableFilter, self).get_context_data(**kwargs)
        context['form'] = FilterForm(initial={'filter': TableFilter.query})
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        qs = self.queryset
        if TableFilter.query:
            terms = TableFilter.query.split(None)
            for term in terms:
                qs = qs.filter(Q(title__icontains=term) |
                                Q(text__icontains=term))
        self.filterset = EntryFilterSet(qs, self.request.GET)
        return self.filterset.qs

#    def get_queryset(self):
#        """By default search all Char and Text fields."""
#        if TableFilter.query:
#            for
#            self.queryset.filter
#        return self.filterset(self.queryset, self.request.GET).qs

#    def get_success_url(self):
#        return self.template_name