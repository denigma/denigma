# Create your views here.
from models import Profile
from django.http import HttpResponse
from django.shortcuts import render_to_response


def whoiswho(request):
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
 
def list(request):
    """Lists all users."""
    users = Profile.objects.all()
    return render_to_response('experts/list.html', {'users':users})
