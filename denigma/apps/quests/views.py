from django.shortcuts import render

from data.models import Entry


def index(request):
    print("quests.index")
    entries = Entry.objects.filter(parent__title="Quests")
    quests = Entry.objects.get(title="Quests")
    return render(request, 'quests/index.html',
        {'entries': entries, 'quests': quests})
