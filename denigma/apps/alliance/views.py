from django.shortcuts import render
from django.views.generic import ListView, DetailView

from data import get
from data.views import EntryView, EntryList
from data.models import Entry

from experts.models import Collaboration


def index(request, template="alliance/homepage.html"):
    about, manifesto, take_action = get('About the Alliance'), get('ILA Manifesto'), get('Take Action')
    news = Entry.objects.filter(tags__name='alliance').order_by('-created')[:5]
    ctx = {'about': about,
           'manifesto': manifesto,
           'take_action': take_action,
           'news': news}
    return render(request, template, ctx)


class DataUnitView(EntryView):
    template_name = "alliance/entry_detail.html"


class DataList(EntryList):
    template_name = "alliance/entry_list.html"
    queryset = Entry.objects.filter(tags__name="alliance").order_by('-created')


class ProjectView(ListView):
    template_name = "alliance/project_list.html"
    queryset = Collaboration.objects.filter(labs__title="International Longevity Alliance")

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['entry'] = get('Projects')
        return context


class ProjectDetail(DetailView):
    template_name = "alliance/project_detail.html"
    model = Collaboration

