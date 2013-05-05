# Create your views here.

from django import forms
from django.shortcuts import render




class GbAForm(forms.Form):
    taxid = forms.CharField()
    seed_list = forms.CharField(widget=forms.Textarea())



def gba(request):
    if request.method == 'POST':
        from gba import algorithm
        form = GbAForm(request.POST)
        if form.is_valid():
            taxid = form.cleaned_data['taxid']
            seed_list = form.cleaned_data['seed_list']
            d = algorithm(seed_list.split('\n'), int(taxid), n='undirected')
    else:
        form = GbAForm()
        d = {}
    return render(request, 'network/index.html', {'form': form, 'results': d})

#@permission_required('is_superuser')
def delete_candidates(request):
    num_candidates = Candidate.objects.all().count()
    #num_profiles = len(profiles)
    if num_candidates:
        #profiles.delete()
        statement = 'TRUNCATE TABLE candidate'
        cursor = connection.cursor()
        cursor.execute(statement)

        message_type = messages.SUCCESS
    else:
        message_type = messages.WARNING
    msg = "Deleted %s profiles." % num_candidates
    messages.add_message(request, message_type, ugettext(msg))
    return redirect('/expressions/')