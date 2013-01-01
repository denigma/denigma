# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User, AnonymousUser
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

import reversion

from add.forms import handlePopAdd

from data.filters import TableFilter
from data.views import Create, Update
from meta.view import log
from data import get
from links.models import Link
from datasets.models import Reference

from models import Profile, Collaboration
from filters import ProfileFilterSet, CollaborationFilterSet
from tables import ProfileTable, CollaborationTable
from forms import ProfileForm, CollaborationForm


def whoiswho(request):
    """Intended to synchronize Experts with the WhoisAge.""" 
    profiles = [data.user_name for profile in Profile.objects.all()]
    
    from experts import main
    experts = main()
    for expert in experts.values():
        
        # Change name to user_name:
        expert = dict([(k,v) for k,v in vars(expert).items() if v]) # Removes none fields to prevent lsoe of data by updating. 
        expert['user_name'] = expert.pop('name')# del expert['name'] http://stackoverflow.com/questions/4406501/change-the-key-value-in-python-dictionary

        if expert['user_name'] not in datas:
            profile = Profile(**expert)
            data.save()
        else:
            Profile.objects.filter(user_name=expert['user_name']).update(**expert)
            
    return HttpResponse("WhoIsWho completed (%s experts)" % len(experts))

def index(request, template='experts/index.html'):
    entry = get('Experts')
    return render(request, template, {'entry': entry})

def archive(request, template='experts/profiles.html'):
    """Lists all experts."""
    experts = Profile.objects.all()
    return render(request, template, {'experts':experts})

def detail(request, expertname, template='experts/detail.html'):
    """Shows the detail view of an expert."""
    try:
        expert = Profile.objects.get(user_name=expertname.replace('_', ' '))
    except Profile.DoesNotExist:
        expert = Profile.objects.get(pk=expertname)
    references = Reference.objects.filter(authors__icontains=expert.last_name)
    return render(request, template, {'expert': expert, 'references': references})


class ProfileList(TableFilter):
    queryset = Profile.objects.all()
    success_url = '/experts/profiles/'
    model = Profile
    table_class = ProfileTable

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileList, self).get_context_data(*args, **kwargs)
        context['entry'] = get('Expert')
        return context

    def get_queryset(self):
        qs = self.queryset.order_by('user_name')
        if ProfileList.query:
            terms = ProfileList.query.split(None)
            for term in terms:
                qs = qs.filter(Q(first_name__contains=term) |
                               Q(last_name__icontains=term) |
                               Q(email__icontains=term) |
                               Q(affiliation__icontains=term) |
                               Q(work__icontains=term))
        self.filterset = ProfileFilterSet(qs, self.request.GET)
        return self.filterset.qs

class CollaborationList(TableFilter):
    table_class = CollaborationTable
    model = Collaboration
    queryset = Collaboration.objects.all()
    success_url = '/experts/collaborations/'

    def get_context_data(self, *args, **kwargs):
        context = super(CollaborationList, self).get_context_data(*args, **kwargs)
        context['entry'] = get('Collaboration')
        return context

    def get_queryset(self):
        qs = self.queryset
        if CollaborationList.query:
            terms = CollaborationList.query.split(None)
            for term in terms:
                qs = qs.filter(Q(project__title__icontains=term) |
                               Q(labs__title__icontains=term) |
                               Q(members__user_name__icontains=term))
        self.filterset = CollaborationFilterSet(qs, self.request.GET)
        return self.filterset.qs

class CreateProfile(Create):
    model = Profile
    form_class = ProfileForm
    comment = "Created profile"
    message = 'Successfully created %s'

    def form_valid(self, form):
        with reversion.create_revision():
            self.object = form.save(commit=False)
            if isinstance(self.request.user, AnonymousUser):
                self.request.user = User.objects.get(username='Anonymous')
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.comment = comment
            self.object.save()
            log(self.request, self.object, comment, 1)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.success_url or self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


class UpdateProfile(Update):
    model = Profile
    form_class = ProfileForm
    comment = "Updated profile"
    message = 'Successfully updated %s'

    def form_valid(self, form):
        with reversion.create_revision():
            self.object = form.save(commit=False)
            print("self.object: %s" % self.object)
            if isinstance(self.request.user, AnonymousUser):
                self.request.user = User.objects.get(username='Anonymous')
            comment = self.request.POST['comment'] or self.comment
            reversion.set_comment(comment)
            self.object.comment = comment
            self.object.save()
            log(self.request, self.object, comment, 2)
            reversion.set_user(self.request.user)
            form.save_m2m()
            self.success_url = self.success_url or self.object.get_absolute_url()
            messages.add_message(self.request, messages.SUCCESS,
                _(self.message % self.object))
            return HttpResponseRedirect(self.get_success_url())


def newProfile(request):
    return handlePopAdd(request, ProfileForm, 'contacts')


class CreateCollaboration(Create):
    model = Collaboration
    success_url = '/experts/collaborations/'
    form_class = CollaborationForm
    comment = "Created Collaboration"
    message = "Successfully created collaboration"


class UpdateCollaboration(Update):
    model = Collaboration
    success_url = '/experts/collaborations/'
    form_class = CollaborationForm
    comment = "Updated Collaboration"
    message = "Successfully updated Collaboration"


