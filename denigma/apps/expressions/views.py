from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.utils.translation import ugettext
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django_tables2 import RequestConfig

from lifespan.models import Regimen
from annotations.models import Species, Tissue

from models import Replicate, Profile, Transcript, Signature, Expression
from forms import ProfileForm, SignatureForm
from tables import TranscriptTable, ReplicateTable
from filters import TranscriptFilterSet

from blog.models import Post
from utils import stats

def transcripts(request):
    filterset = TranscriptFilterSet(request.GET or None)
    return render_to_response('expressions/transcripts.html',
        {'filterset': filterset}, context_instance=RequestContext(request))

def transcript_list(request):
    f = TranscriptFilterSet(request.GET, queryset=Transcript.objects.all())
    return render_to_response('expressions/transcripts.html', {'filter': f},
        context_instance=RequestContext(request))

#234567891123456789212345678931234567894123456789512345678961234567897123456789
def data(title):
    """Fetches a database entry arcording to its title."""
    try:
        entry = Post.objects.get(title=title)
    except (Post.DoesNotExist, Post.MultipleObjectsReturned) as e:
        entry = e
    return entry

def index(request):
    try:
        entry = Post.objects.get(title="Expressions")
    except Post.DoesNotExist as e:
        entry = e
    return render_to_response('expressions/index.html', {'entry': entry},
                             context_instance=RequestContext(request))

def profiles(request):
    profiles = Profile.objects.all()
    ctx = {'entry': data("Profiles"), 'profiles': profiles}
    return render_to_response('expressions/profiles.html', ctx,
        context_instance=RequestContext(request))

def signatures(request):
    signatures = Signature.objects.all()
    ctx = {'entry': data("Signatures"), 'signatures': signatures}
    return render_to_response('expressions/signatures.html', ctx,
        context_instance=RequestContext(request))

def signature(request, pk, ratio=2., pvalue=0.05):
    signature = Signature.objects.get(pk=pk)
    transcripts = signature.transcripts.all()
    filter = TranscriptFilterSet(request.GET, transcripts)
    table = TranscriptTable(transcripts)
    RequestConfig(request).configure(table)
    transcripts_up = transcripts.filter(Q(ratio__gt=ratio) & Q(pvalue__lt=pvalue))
    transcripts_down = transcripts.filter(Q(ratio__lt=1/ratio) & Q(pvalue__lt=pvalue))
    ctx = {'signature': signature, 'transcripts': transcripts,
           'transcripts_up': transcripts_up,
           'transcripts_down': transcripts_down,
           'table': table,
           'ratio': ratio,
           'pvalue': pvalue,
           'filter': filter}
    return render_to_response('expressions/signature.html', ctx,
        context_instance=RequestContext(request))


def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    replicates = profile.replicates.all()
    table = ReplicateTable(replicates)
    RequestConfig(request).configure(table)
    ctx = {'profile': profile, 'replicates': replicates}
    return render_to_response('expressions/profile.html', ctx,
        context_instance=RequestContext(request))

@login_required
def add_profile(request):
    form = ProfileForm(request.POST or None, request.FILES or None)

    if request.POST:
        if not "file" in request.POST:
            file = request.FILES['file']
            data = file.read().split('\n')
        elif request.POST["data_text"]:
            data = request.POST["data_text"].replace('\r', '').split('\n')
        else:
            redirect('/expressions/profile/add/')

        # Create profiles:
        profiles = []

        for line in data:
            columns = line.split('\t')
            if not line: continue
            if line == data[0]:
                header = columns

                for index, dataset in enumerate(header[1:]):
                    tissue, diet, name = columns[index+1].split('_')
                    print tissue, diet, name
                    profile = Profile(
                        name=name,
                        species=Species.objects.get(pk=request.POST['species']),
                        diet=Regimen.objects.get(shortcut__exact=diet)
                    )
                    profile.save()
                    tissues = Tissue.objects.filter(notes__icontains=tissue)
                    profile.tissue = tissues
                    profiles.append(profile)
                continue

            # Iterate over columns and save the replicates:
            probe_id = columns[0]
            for index, column in enumerate(columns[1:]):
                intensity = columns[index+1]
                replicate = Replicate(probe_id=probe_id, intensity=intensity)
                replicate.save()
                profiles[index].replicates.add(replicate)
        msg = "Successfully integrated profiles."
        messages.add_message(request, messages.SUCCESS, ugettext(msg))
        redirect('/expressions/profile/')

    ctx = {'form': form, 'action': 'Add'}
    return render_to_response('expressions/profile_form.html',ctx,
        context_instance=RequestContext(request))

@login_required
def add_signature(request):
    """The aim is to retrieve a list of differential expressed genes for certain
    criteria (e.g. fold_change, p-value, tissue).
    """
    form = SignatureForm(request.POST or None, request.FILES or None)
    if request.POST:
        if not "file" in request.POST:
            file = request.FILES['file']
            data = file.read().split('\n')
        elif "profile" not in request:
            msg = "No file or profiles selected. Please provide either a signature "\
                  "file to upload or select profiles to derive a signature."
            messages.add_message(request, messages.ERROR, ugettext(msg))
            return redirect('/expressions/signature/add/')

        # Inferre descriptive informations from the filename:
        if file.name.startswith('name='):
            info = dict([item.split('=') for item in file.name.split(';')])
        if 'tissue' in info:
            tissues = info['tissue'].replace(', ', '@').replace(' and ', '@').split('@') # @ is unlikey to be used as filename.
        else:
            tissues = request.POST.getlist('tissues')
        if "diet" in info:
            regimen = Regimen.objects.get(shortcut__exact=info['diet'])

        # Species from form:
        try:
            species = Species.objects.get(pk=request.POST['species'])
        except ValueError as e:
            msg = "Species not found in Denigma db. %s. Please select a species." % e
            messages.add_message(request, messages.ERROR, ugettext(msg))
            return redirect('/expressions/signature/add/')

        # Create signature:
        signature = Signature(name=request.POST['name'] or info['name'], diet=regimen, species=species)#,
        signature.save()

        # Adding tissues:
        for tissue in tissues:
            try:
                tissue = Tissue.objects.get(pk=tissue) #if it is selcted from form
            except:
                print "Did not found tissue by pk."
                try:
                    tissue = Tissue.objects.get(name__iexact=tissue) # If it is inferred from file name.
                except Tissue.DoesNotExist as e:
                    messages.add_message(request, messages.ERROR, ugettext("%s: %s" % (str(e)[:-1], tissue)))
                    return redirect('/expressions/signature/add/')

            signature.tissues.add(tissue)
        print "Tissues:", signature.tissues.all()



        header = {}
        for index, column in enumerate(data[0].split('\t')):
            if "DR" in column: column = "exp"
            elif "AL" in column: column = "ctr"
            header[column.lower().replace('gene symbol', 'symbol')\
                                 .replace('gene_symbol', 'symbol')\
                                 .replace(' ', '_')] = index

        # For effect size
        ctr_values = []
        exp_values = []

        #num_lines = len(data); counter = 0
        for line in data[1:]:
            #counter += 1
            if not line: continue
            columns = line.split('\t')
            if len(columns) <= 5: break #continue
            seq_id = columns[header['seq_id']]
            pvalue = columns[header['p_value']]
            symbol = columns[header['symbol']]
            fold_change = columns[header['fold_change']]
            ctr = columns[header['ctr']]
            exp = columns[header['exp']]

            # Calculating effect size:
            for k,v  in header.items():
                if k.startswith('ctr'):
                    ctr_values.append(float(columns[v]))
                elif k.startswith('exp'):
                    exp_values.append(float(columns[v]))
            es = stats.effect_size(exp_values, ctr_values)

            transcript = Transcript(seq_id=seq_id, symbol=symbol, ratio=fold_change, pvalue=pvalue, effect_size=es)
            try:
                transcript.save()
                expression = Expression.objects.create(
                    signature=signature,
                    transcript=transcript,
                    exp=exp, ctr=ctr,
                    ratio=fold_change,
                    pvalue=pvalue,
                    effect_size=es)
            except ValueError as e:
                print e, symbol, seq_id, fold_change, pvalue, ctr, exp

        #print "Counter=%s; Number of lines:%s" % (counter, num_lines)
        #if counter == num_lines:
        msg = "Successfully integrated signature: %s" % signature.name
        msg_type = messages.SUCCESS
        #else:
        #    msg = "File upload failed."
        #    msg_type = messages.ERROR
        messages.add_message(request, msg_type, ugettext(msg))
        redirect('/expressions/signatures/')

    ctx = {'form': form, 'action': 'Add'}
    return render_to_response('expressions/signature_form.html', ctx,
        context_instance=RequestContext(request))

@permission_required('is_superuser')
def delete_profiles(request):
    profiles = Profile.objects.all()
    num_profiles = len(profiles)
    if profiles:
        profiles.delete()
        message_type = messages.SUCCESS
    else:
        message_type = messages.WARNING
    msg = "Deleted %s profiles." % num_profiles
    messages.add_message(request, message_type, ugettext(msg))
    return redirect('/expressions/')

@permission_required('is_superuser')
def delete_replicates(request):
    replicates = Replicate.objects.all()
    num_replicates = len(replicates)
    replicates.delete()
    if num_replicates:
        message_type = messages.SUCCESS
    else:
        message_type = messages.WARNING
    msg = "Deleted %s replicates." % num_replicates
    messages.add_message(request, message_type, ugettext(msg))
    return redirect('/expressions/')

@permission_required('is_superuser')
def delete_signatures(request):
    signatures = Signature.objects.all()
    num_signatures = len(signatures)
    if signatures:
        signatures.delete()
        message_type = messages.SUCCESS
    else:
        message_type = messages.WARNING
    msg = "Deleted %s signatures." % num_signatures
    messages.add_message(request, messages.SUCCESS, ugettext(msg))
    return redirect('/expressions/')

@permission_required('is_superuser')
def delete_signature(request, pk):
    signature = Signature.objects.get(pk=pk)
    transcripts = signature.transcripts.all()
    transcripts.delete()
    #for transcript in signature.transcripts.all():
    #    transcript.delete()
    signature.delete()
    msg = "Successfully delete signature %s" % signature.name
    messages.add_message(request, messages.SUCCESS, ugettext(msg))
    return redirect('/expressions/signatures/')

@permission_required('is_superuser')
def delete_transcripts(request):
    transcripts = Transcript.objects.all()
    num_transcripts = len(transcripts)
    if transcripts:
        transcripts.delete()
        message_type = messages.SUCCESS
    else:
        message_type = messages.WARNING
    msg = "Deleted %s transcripts." % num_transcripts
    messages.add_message(request, message_type, ugettext(msg))
    return redirect('/expressions/')

class ProfileCreate(CreateView):
    context_object_name='profile'
    form_class = ProfileForm
    model = Profile


class SignatureCreate(CreateView):
    form_class = SignatureForm
    model = Signature



#    profiles = Profile.objects.all()
#    for profile in profiles:
#        for replicate in
#
#    signature = Signature.object.get(tissue="malipihigian")
#    for gene in signature.genes
#    gene