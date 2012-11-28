from django.forms import Form, CharField
from django.views.generic.edit import FormView

from django_tables2 import SingleTableView


class FilterForm(Form):
    filter = CharField()

class TableFilter(SingleTableView, FormView):
    form_class = FilterForm
    query = None
    filterset = None
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
        print self.filterset
        context['filterset'] = self.filterset
        return context

#    def get_queryset(self):
#        """By default search all Char and Text fields."""
#        if TableFilter.query:
#            for
#            self.queryset.filter
#        return self.filterset(self.queryset, self.request.GET).qs

#    def get_success_url(self):
#        return self.template_name