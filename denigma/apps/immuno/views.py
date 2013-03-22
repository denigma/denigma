from django.views.generic import TemplateView
from django.db.models import Q

from data import get
from data.models import Entry
from data.views import EntryView


class IndexView(TemplateView):
    template_name='immuno/base.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()
        context['finding_aging_factors'] = get('Finding Aging Factors')
        context['finding_aging_factors'].text = "We provide blood testing to identify the factors causes aging."
        context['crowd_funding_lifespan_extension'] = get('Crowd Funding Lifespan Extension')
        context['crowd_funding_lifespan_extension'].text = "We are a lab of professional researches dedicated to solve aging. Please support us."
        context['immunosenescence'] = get('Immunosenescence')
        context['immunosenescence'].text = "The immune system deteriorates with increasing age. We can prevent it."
        context['lab'] = get('Pathophysiology and Immunology Laboratory')
        context['group'] = get('Pathophysiology and Immunology Group')
        context['immunosenescence'].text = "A highly skilled team of enthusiastic researches."
        context['publications'] = get('Publications')
        context['crowd_funding'] = get('Crowd-Funding')
        context['experiments'] = get('Experiments')
        context['entries'] = Entry.objects.filter(Q(tags__name='immunology') | Q(tags__name='immune system')).distinct().order_by('-created')
        return context






class DetailView(EntryView):
    template_name = 'immuno/entry_detail.html'


class View(TemplateView):
    template_name='immuno/detail.html'

    def dispatch(self, request, *args, **kwargs):
        if "slug" in kwargs:
            self.title = kwargs['slug'].title().replace('-', ' ')
        return super(View, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(View, self).get_context_data()
        context['object'] = get(self.title)
        return context


class AboutView(View):
    template_name='immuno/about.html'


class ContactView(View):
    template_name='immuno/contact.html'


