from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from models import Profile
from filters import ProfileFilterSet
from tables import ProfileTable
from forms import ProfileForm

from data.filters import TableFilter
from data.views import Create, Update


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
    """Lists all experts."""
    experts = Profile.objects.all()
    return render(request, template, {'experts':experts})

def detail(request, expertname, template='experts/detail.html'):
    """Shows the detail view of an expert."""
    try:
        expert = Profile.objects.get(user_name=expertname.replace('_', ' '))
    except Profile.DoesNotExist:
        expert = Profile.objects.get(pk=expertname)
    return render(request, template, {'expert': expert})


class ProfileList(TableFilter):
    queryset = Profile.objects.all()
    success_url = '/experts/'
    model = Profile
    table_class = ProfileTable

    def get_queryset(self):
        qs = self.queryset
        print ProfileList.query
        if ProfileList.query:
            terms = ProfileList.query.split(None)
            for term in terms:
                qs = qs.filter(Q(first_name__contains=term) |
                               Q(last_name__icontains=term) |
                               Q(email__icontains=term) |
                               Q(affliation__icontains=term) |
                               Q(work__icontains=term))
                print term, qs.count()
        self.filterset = ProfileFilterSet(qs, self.request.GET)
        print self.filterset.qs.count()
        return self.filterset.qs


class CreateProfile(Create):
    model = Profile
    success_url = '/experts/'
    form_class = ProfileForm
    comment = "Created profile"
    message = 'Successfully created %s'


class UpdateProfile(Update):
    model = Profile
    success_url = '/experts/'
    form_class = ProfileForm
    comment = "Updated profile"
    message = 'Successfully updated %s'