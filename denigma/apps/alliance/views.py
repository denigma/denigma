from django.shortcuts import render
from django.views.generic import ListView, DetailView

from data import get
from data.views import EntryView, EntryList
from data.models import Entry

from experts.models import Collaboration


def index(request, template="alliance/homepage.html"):
    about, manifesto, take_action = get('About the Alliance'), get('ILA Manifesto'), get('Take Action')
    news = Entry.objects.filter(tags__name='alliance').order_by('created')
    ctx = {'about': about,
           'manifesto': manifesto,
           'take_action': take_action,
           'news': news}
    return render(request, template, ctx)


class DataUnitView(EntryView):
    template_name = "alliance/entry_detail.html"


class DataList(EntryList):
    template_name = "alliance/entry_list.html"
    queryset = Entry.objects.filter(tags__name="alliance")


class ProjectView(ListView):
    template_name = "alliance/project_list.html"
    queryset = Collaboration.objects.filter(labs__title__istartswith="Inte")


class ProjectDetail(DetailView):
    template_name = "alliance/project_detail.html"
    model = Collaboration

