from itertools import chain

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.utils.translation import ugettext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection
from django.db.models import Q
from django.db import transaction

from django_tables2 import RequestConfig

from lifespan.models import Regimen
from annotations.models import Species, Tissue

from models import Replicate, Profile, Transcript, Signature, Expression, Probe, Set, Gene
from forms import ProfileForm, SignatureForm, SetForm
from tables import TranscriptTable, ReplicateTable, AnnotationTable
from filters import TranscriptFilterSet

from blog.models import Post
from data import get

from stats.effective import effect_size
from stats.pValue import t_two_sample, calc_benjamini_hochberg_corrections, hyperg
from annotations.david.report import enrich
from annotations.mapping import mapid
from utils.count import Counter


IDs = ['seq_id', 'entrez_gene_id']

def functional_enrichment(terms, transcripts,  id='seq_id'):
    """Helper function to create annotation tables for functional enrichment."""
    if terms:
        # Functional Annotation:
        ## Determine seq_id type:
        if isinstance(transcripts, (set, list)):
            for e in transcripts:
                try:
                    entity_id = transcripts[0].seq_id
                    ids = [transcript.seq_id for transcript in transcripts if transcript.seq_id]
                except:
                    ids = transcripts
                    entity_id = e # What happens if list is empty?
                break
        else:
            entity_id = transcripts[0].seq_id
            ids = [transcript.seq_id for transcript in transcripts if transcript.seq_id]
        if id != 'seq_id':
            idType = id.upper()
        else:
            if entity_id.startswith('FBtr'):
                idType = 'ENSEMBL_TRANSCRIPT_ID'
            else:
                idType = 'ENSEMBL_GENE_ID'
        print idType
        ## Create tables:
        if transcripts:
            terms = enrich(ids, idType=idType )
            table = AnnotationTable(terms.data())
        else:
            table = None
    else:
        table = None
    return table

def transcripts(request):
    filterset = TranscriptFilterSet(request.GET or None)
    return render_to_response('expressions/transcripts.html',
        {'filterset': filterset}, context_instance=RequestContext(request))

def transcript_list(request):
    f = TranscriptFilterSet(request.GET, queryset=Transcript.objects.all())
    return render_to_response('expressions/transcripts.html', {'filter': f},
        context_instance=RequestContext(request))

def index(request):
    entry = get("Expressions")
    return render_to_response('expressions/index.html', {'entry': entry},
                             context_instance=RequestContext(request))

def profiles(request):
    profiles = Profile.objects.all()
    ctx = {'entry': get("Profiles"), 'profiles': profiles}
    return render_to_response('expressions/profiles.html', ctx,
        context_instance=RequestContext(request))

def signatures(request):
    signatures = Signature.objects.all()
    ctx = {'entry': get("Signatures"), 'signatures': signatures}
    return render_to_response('expressions/signatures.html', ctx,
        context_instance=RequestContext(request))

def signature(request, pk=None, ratio=2., pvalue=0.05, fold_change=None, exp=None, benjamini=None, name=None):
    terms = False
    id = 'seq_id'
    if request.GET:
        if 'ratio' in request.GET and request.GET['ratio']:
            ratio = float(request.GET['ratio'])
        if 'pvalue' in request.GET and request.GET['pvalue']:
            pvalue = float(request.GET['pvalue'])
        if 'benjamini' in request.GET and request.GET['benjamini']:
            benjamini = float(request.GET and request.GET['benjamini'])
        if 'expression__exp' in request.GET and request.GET['expression__exp']:
            exp = float(request.GET['expression__exp'])
        if 'id' in request.GET and request.GET['id']:
            id = request.GET['id']
        if 'terms' in request.GET and request.GET['terms']:
            terms = True
        else:
            terms = False
    if pk: signature = Signature.objects.get(pk=pk)
    elif name:  signature = Signature.objects.get(name=name)

    if not exp:
        transcripts = signature.transcripts.filter((Q(ratio__gt=ratio)
                                                    | Q(ratio__lt=1./ratio))
                                                    & Q(pvalue__lt=pvalue))
    else: # What is about a gene that is only low expressed in one condition?
        #print "Filtering on expression:"
        transcripts = signature.transcripts.filter((Q(ratio__gt=ratio)
                                                    | Q(ratio__lt=1./ratio))
                                                    & Q(pvalue__lt=pvalue
                                                    #& Q(expression__exp__gt=exp) & Q(expression__ctr__gt=exp)
                                                    ))

        transcripts = transcripts.filter(expression__exp__gt=exp,
                                         expression__ctr__gt=exp)
    if request.GET:
        if 'symbol' in request.GET and request.GET['symbol']:
            symbol = request.GET['symbol']
            transcripts = transcripts.filter(symbol__icontains=symbol)
        if 'fold_change' in request.GET and request.GET['fold_change']:
            fold_change = float(request.GET['fold_change'])
            #print len(transcripts)

            transcripts = transcripts.filter(Q(fold_change__gt=fold_change)
                                           | Q(fold_change__lt=1./fold_change))
            #print "filtered transcripts", len(transcripts)

        if 'benjamini' in request.GET and request.GET['benjamini']:
            benjamini = float(request.GET['benjamini'])
            transcripts = transcripts.filter(benjamini__lt=benjamini)


    filter = TranscriptFilterSet(request.GET, transcripts)
    #print type(filter), vars(filter)
    #print len(filter.queryset)
    table = TranscriptTable(filter.queryset)
    RequestConfig(request).configure(table)
    transcripts_up = transcripts.filter(Q(ratio__gt=ratio)
                                        & Q(pvalue__lt=pvalue))

    transcripts_down = transcripts.filter(Q(ratio__lt=1./ratio)
                                          & Q(pvalue__lt=pvalue))

    table_up = functional_enrichment(terms, transcripts_up)
    table_down = functional_enrichment(terms, transcripts_down)
    table_diff = functional_enrichment(terms, list(chain(transcripts_up, transcripts_down)))

    #print id
    transcripts_up = set([getattr(transcript, id) for transcript in transcripts_up])
    if None in transcripts_up: transcripts_up.remove(None)
    transcripts_down = set([getattr(transcript, id) for transcript in transcripts_down])
    if None in transcripts_down: transcripts_down.remove(None)
    #transcripts_diff = set([getattr(transcripts, id) for transcript in transcripts_diff])
    #if None in transcripts_diff: transcripts_diff.remove(None)

    ctx = {'signature': signature, 'transcripts': transcripts,
           'transcripts_up': transcripts_up,
           'transcripts_down': transcripts_down,
           #'transcripts_diff': transcripts_diff,
           'table': table,
           'ratio': ratio,
           'pvalue': pvalue,
           'benjamini': benjamini,
           'filter': filter,
           'terms': terms,
           'table_up': table_up,
           'table_down': table_down,
           'table_diff': table_diff,
           'ids': IDs,
           'id': id
    }
    return render_to_response('expressions/signature.html', ctx,
        context_instance=RequestContext(request))


class Signatures(list):
    def __init__(self, signatures):
        self._diff = []
        self._up = []
        self._down = []
        self.diff = []
        self.up = []
        self.down = []
        for signature in signatures:
            #print signature.difference
            self._diff.append(signature.difference)
            #print type(self._diff), len(self._diff), self._diff
            self._up.append(signature.up)
            self._down.append(signature.down)
        self.diff = set(self._diff[0]).intersection(*self._diff)
        self.up = set(self._up[0]).intersection(*self._up)
        self.down = set(self._down[0]).intersection(*self._down)


class Intersection(object):
    def __init__(self, a_signature, another_signature):
        self.a = a_signature
        self.another = another_signature
        self.name = "%s <-> %s" % (a_signature.link, another_signature.link)
        self.up = a_signature.up & another_signature.up
        self.down = a_signature.down & another_signature.down
        self.diff = (a_signature.up | a_signature.down) \
                    & (another_signature.up | another_signature.down)

        self.diff_pvalue = hyperg(len(a_signature.diff), len(another_signature.diff), a_signature.transcripts.count(), len(self.diff))
        self.down_pvalue = hyperg(len(a_signature.down), len(another_signature.down), a_signature.transcripts.count(), len(self.down))
        self.up_pvalue = hyperg(len(a_signature.up), len(another_signature.up), a_signature.transcripts.count(), len(self.up))

        self.anti_a = a_signature.up & another_signature.down
        self.anti_b = a_signature.down & another_signature.up

        self.anti_a_pvalue = hyperg(len(a_signature.up), len(another_signature.down), a_signature.transcripts.count(), len(self.anti_a))
        self.anti_b_pvalue = hyperg(len(a_signature.down), len(another_signature.up), a_signature.transcripts.count(), len(self.anti_b))

    def differential(self):
        return self.diff #" ".join()

    def upregulated(self):
        return self.up #" ".join()

    def downregulated(self):
        return self.down# " ".join()



def intersections(request, ratio=2., pvalue=0.05, fold_change=None, exp=None, set=None, benjamini=None):
    entry = get("Intersections")
    id = 'seq_id'
    if request.GET:
        if 'ratio' in request.GET and request.GET['ratio']:
            ratio = float(request.GET['ratio'])
        if 'pvalue' in request.GET and request.GET['pvalue']:
            pvalue = float(request.GET['pvalue'])
        if 'fold_change' in request.GET and request.GET['fold_change']:
            fold_change = float(request.GET['fold_change'])
        if 'benjamini' in request.GET and request.GET['benjamini']:
            benjamini = float(request.GET['benjamini'])
        if 'expression__exp' in request.GET and request.GET['expression__exp']:
            exp = request.GET['expression__exp']
            print "Expression exp"
        if 'set' in request.GET and request.GET['set']:
            set = request.GET['set']
        if 'id' in request.GET and request.GET['id']:
            id = request.GET['id']

    filter = TranscriptFilterSet(request.GET, transcripts)

    intersections = []
    #signatures = Signature.objects.differential(ratio, pvalue)      #
    if set:
        set = Set.objects.get(pk=set)
        signatures = set.signatures.all()
    else:
        set = Set.objects.get(pk=1)
        signatures = set.signatures.all()
    for signature in signatures:              #
        signature.differential(ratio, pvalue, fold_change, exp, benjamini, id) # Might a good function for a custom manager.
    for a_signature in signatures:
        for another_signature in signatures[:len(signatures)]: # Prevents duplicated comparisions the other way around.
            if a_signature != another_signature: # Prevent comparision of the same signatures and
                intersection = Intersection(a_signature, another_signature)
                #print intersection.name, len(intersection.up), len(intersection.down)
                intersections.append(intersection)

    # Context:
    ctx = {'title': 'Intersections',
           'entry': entry,
           'signatures': signatures,
           'intersections': intersections,
           'ratio': ratio,
           'pvalue': pvalue,
           'benjamini': benjamini,
           'fold_change': fold_change,
           'exp': exp,
           'filter': filter,
           'sets': Set.objects.all(),
           'ids': IDs,
           'id': id,
    }
    return render_to_response('expressions/intersections.html', ctx,
        context_instance=RequestContext(request))

def intersection(request, a, another, ratio=2., pvalue=0.05,
                 fold_change=None, exp=None, benjamini=None):
    terms = None
    id ='seq_id'
    a_signature = Signature.objects.get(pk=a)

    another_signature = Signature.objects.get(pk=another)

    if request.GET:
        if 'ratio' in request.GET and request.GET['ratio']:
            ratio = request.GET['ratio']
        if 'pvalue' in request.GET and request.GET['pvalue']:
            pvalue = request.GET['pvalue']
        if 'benjamini' in request.GET and request.GET['benjamini']:
            benjamini = request.GET['benjamini']
        if 'fold_change' in request.GET and request.GET['fold_change']:
            fold_change = request.GET['fold_change']
            print "get fold_change", fold_change
        if 'expression__exp' in request.GET and request.GET['expression__exp']:
            exp = float(request.GET['expression__exp'])
        if 'id' in request.GET and request.GET['id']:
            id = request.GET['id']
        if 'terms' in request.GET and request.GET['terms']:
            terms = True
        else:
            terms = False

    filter = TranscriptFilterSet(request.GET, transcripts)

    if fold_change == 'None':
        fold_change = None
    #print fold_change

    a_signature.differential(float(ratio), float(pvalue),
                             float(fold_change or 0), exp, benjamini, id)
    another_signature.differential(float(ratio), float(pvalue),
                                  float(fold_change or 0), exp, benjamini, id)
    intersection = Intersection(a_signature, another_signature)

    table_up = functional_enrichment(terms, intersection.upregulated(), id)
    table_down = functional_enrichment(terms, intersection.downregulated(), id)

    ctx = {'title': '%s & %s' % (a_signature, another_signature),
           'intersection': intersection,
           'a_signature': a_signature,
           'another_signature': another_signature,
           'filer': filter,
           'terms': terms,
           'table_up': table_up,
           'table_down': table_down,
           'ids': IDs,
           'id': id,
    }
    return render_to_response('expressions/intersection.html/', ctx,
        context_instance=RequestContext(request))

def meta(request, ratio=2., pvalue=0.05, fold_change=None, exp=None, set=None, benjamini=None):
    """Common to all signature in a category."""
    terms = False
    id = 'seq_id'
    if request.GET:
        if 'ratio' in request.GET and request.GET['ratio']:
            ratio = float(request.GET['ratio'])
        if 'pvalue' in request.GET and request.GET['pvalue']:
            pvalue = float(request.GET['pvalue'])
        if 'benjamini' in request.GET and request.GET['benjamini']:
            benjamini = float(request.GET['benjamini'])
        if 'fold_change' in request.GET and request.GET['fold_change']:
            fold_change = float(request.GET['fold_change'])
        if 'expression__exp' in request.GET and request.GET['expression__exp']:
            exp = float(request.GET['expression__exp'])
        if 'set' in request.GET and request.GET['set']:
            set = request.GET['set']
        if 'terms' in request.GET and request.GET['terms']:
            terms = True
        if 'id' in request.GET['id'] and request.GET['id']:
            id = request.GET['id']

    entry = get("Meta-Analysis")
    set = Set.objects.get(pk = set or 1)
    signatures = set.signatures.all()
    for signature in signatures:
        signature.differential(ratio, pvalue, fold_change, exp, benjamini, id)
    signatures = Signatures(signatures)
    filter = TranscriptFilterSet(request.GET, transcripts)
    if terms:
        table_up = functional_enrichment(terms, signatures.up, id)
        table_down = functional_enrichment(terms, signatures.down, id)
        #table_diff = functional_enrichment(terms, list(chain(signatures.up, signatures.down, id)))
    else:
        table_up = table_down = table_diff = None
    ctx = {'title': 'Meta-Analysis',
           'entry': entry,
           'signatures': signatures,
           'filter': filter,
           'sets': Set.objects.all(),
           'terms': terms,
           'table_up': table_up,
           'table_down': table_down,
           'table_diff': table_diff,
           'ids': IDs,
           'id': id,
    }
    return render_to_response('expressions/meta.html', ctx,
        context_instance=RequestContext(request))

def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    replicates = Replicate.objects.filter(profile=profile) #profile.replicates.all()
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
        replicates = [] # Container for bulk creation.

        # Header:
        columns = data[0].split('\t')
        for index, dataset in enumerate(columns[1:]):
            tissue, diet, name = columns[index+1].split('_')
            #print tissue, diet, name
            profile = Profile(
                name=name,
                species=Species.objects.get(pk=request.POST['species']),
                diet=Regimen.objects.get(shortcut__exact=diet)
            )
            profile.save()
            tissues = Tissue.objects.filter(notes__icontains=tissue)
            profile.tissue = tissues
            profiles.append(profile)
            #print index, tissue, diet, name

        # Actually Data Parsing:
        limit = 10
        counter = 0
        overall_count = 0
        lines = data[1:]
        line_number = len(lines)
        c = Counter(lines)
        print(line_number)
        for line in lines:
            #print(line)
            counter += 1
            c.count()
            #if counter % 2: print counter
#            if (100. * overall_count / line_number) < 40:
#                overall_count += counter
#                continue
            columns = line.split('\t')
            if not line: continue
            #print("Iterate over columns and save the replicates:")
            probe_id = columns[0]
            for index, column in enumerate(columns[1:]):
                #print index, column
                intensity = columns[index+1]
                replicate = Replicate(probe_id=probe_id, intensity=intensity,
                                      profile=profiles[index])
                #replicate.save()
                replicates.append(replicate)


            if counter >= limit:
                current = 100. * overall_count / line_number
                #print(current)
                #if current > 47 and not current > 48:
                    #print " ".join(replicate.intensity for replicate in replicates)
                    #
                #else:
                try: Replicate.objects.bulk_create(replicates)
                except Exception as e:
                    print(e)
                    messages.add_message(request, messages.ERROR, ugettext("1. Try: "+str(e)))
                    try:
                        [replicate.save() for replicate in replicates]
                    except Exception as es:
                        print(e)
                        messages.add_message(request, messages.ERROR, ugettext("2. Try: "+str(e)))
                replicates = []
                overall_count += counter
                counter = 0
                #print(current)
        if replicates:
            #Replicate.objects.bulk_create(replicates)
            replicates = []
            overall_count += counter

        # Adding replicates:
#        for profile in profiles:
#            replicates = Replicate.objects.filter(profile_id=profile.pk)
#            for replicate in replicates:
#                profile.replicates.add(replicate)
            #profiles[index].replicates.add(replicate)

        msg = "Successfully integrated profiles."
        print(msg)
        messages.add_message(request, messages.SUCCESS, ugettext(msg))

        # Cleaning up:
        request.POST['file'] = ''
        data = ''
        import gc
        gc.collect()
        redirect('/expressions/profiles/')

    ctx = {'form': form, 'action': 'Add'}
    return render_to_response('expressions/profile_form.html',ctx,
        context_instance=RequestContext(request))

#def process_profile(request):
#    for profile in profiles:
#        replicates = profiles.replicates.all()
#        for replicate in replicates
#        profiles.transcripts.replicates
#
#        for transcript in profiles.transcripts.all()
#            replicates = transcript.replicates.all()

@permission_required('is_superuser')
def probes(request):
    profiles = Profile.objects.all()
    for profile in profiles:
        probes = {}
        replicates = Replicate.objects.filter(profile=profile)
        for replicate in replicates:
            if replicate.probe_id not in probes:
                probes[replicate.probe_id] = [replicate.intensity]
            else:
                probes[replicate.probe_id].append(replicate.intensity)
        for id, intensities in probes.items():
            probe = Probe(name=id, expression=sum(intensities)/len(intensities), profile=profile)
            probes[id] = probe
        try:
            Probe.objects.bulk_create(probes.values())
        except Exception as e:
            print(str(e))
            try:
                for probe in probes:
                    probe.save()
            except Exception as e:
                print(str(e))
    print('Done!')
    #return redirect('/expressions/profiles/')
    return HttpResponse("Done")

@permission_required('is_superuser')
def delete_probes(request):
    statement = 'TRUNCATE TABLE expressions_probe'
    cursor = connection.cursor()
    cursor.execute(statement)
    msg = "Successfully deleted %s probes" % " ".join(cursor.fetchall())
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/expressions/profiles/')

@permission_required('is_superuser')
def create_signatures(request):
    """Generates signatures from profiles."""
    # Sort profiles according to tissues
    # compare DR vs. AL.
    profiles = Profile.objects.all()
    #print len(profiles)
    signatures = {}
    for profile in profiles:
        tissues = ' '.join([tissue.name for tissue in profile.tissue.all()])
        print tissues, profile.diet.shortcut
        if tissues not in signatures:
            signatures[tissues] = [None, None]
        if profile.diet.shortcut == 'DR':
            signatures[tissues][0]= profile
        else:
            signatures[tissues][1] = profile
    print signatures

    for tissues, profiles in signatures.items():
        print tissues, profiles
        signature = Signature(name=tissues, species=profiles[0].species, diet=profiles[0].diet)
        signature.save()
        for tissue in profiles[0].tissue.all():
            signature.tissues.add(tissue)
        for profile in profiles:
            #background = []
            profile.transcripts = {}
            probes = Probe.objects.filter(profile=profile)
            for probe in probes:
                if not probe.name.startswith('RANDOM'):
                    transcript_name = probe.name.split('P')[0]
                    if transcript_name not in profile.transcripts:
                        profile.transcripts[transcript_name] = [probe.expression]
                    else:
                        profile.transcripts[transcript_name].append(probe.expression)
                #else: # For background subtraction.
                    #background.append(probe.expression)

        for transcript_name, exp_expression in profiles[0].transcripts.items():
            # If expression too low of e.g. 1/3 of probes, exclude probe.
            # RMA (background subtraction, quantile normalization, and median polishing)
            # Benjamini p-value

            exp = sum(exp_expression)/len(exp_expression)
            ctr_expression = profiles[1].transcripts[transcript_name]
            ctr = sum(ctr_expression)/len(ctr_expression)
            ratio = exp/ctr
            if ratio < 1: fold_change = -(1/ratio)
            else: fold_change = ratio
            if len(exp_expression) == 1 or len(ctr_expression) == 1:
                es = pvalue = None
            else:
                es = effect_size(exp_expression, ctr_expression)
                pvalue = t_two_sample(exp_expression, ctr_expression)[1] # Calculate p-value.

            transcript = Transcript(seq_id=transcript_name,
                                    ratio=ratio,
                                    fold_change=fold_change,
                                    effect_size=es,
                                    pvalue=pvalue)
            transcript.save()
            expression = Expression.objects.create(signature=signature, transcript=transcript,
                                           exp=exp, ctr=ctr, ratio=ratio, fold_change=fold_change,
                                            effect_size=es, pvalue=pvalue)
    print('Done')
    return redirect('/expressions/signatures/')

@login_required
def add_signature(request):
    """The aim is to retrieve a list of differential expressed genes for certain
    criteria (e.g. fold_change, p-value, tissue).
    """
    form = SignatureForm(request.POST or None, request.FILES or None)
    if request.POST:
        if not "file" in request.POST:
            file = request.FILES['file']
            data = file.read().replace('\r', '').split('\n')
        elif "profile" not in request:
            msg = "No file or profiles selected. Please provide either a signature "\
                  "file to upload or select profiles to derive a signature."
            messages.add_message(request, messages.ERROR, ugettext(msg))
            return redirect('/expressions/signature/add/')

        # Inferre descriptive informations from the filename:
        if file.name.startswith('name='):
            info = dict([item.split('=') for item in file.name.split(';')])
        if 'tissue' in info:
            tissues = info['tissue'].replace('-', '@').replace(', ', '@').replace(' and ', '@').split('@') # @ is unlikely to be used as filename.
        else:
            tissues = request.POST.getlist('tissues')
        if 'diet' in request.POST and request.POST['diet']:
            regimen = Regimen.objects.get(pk=request.POST['diet'])
        elif "diet" in info:
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
                tissue = Tissue.objects.get(pk=tissue) #if it is selected from form
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
                                 .replace(' ', '_')\
                                 .replace('platform_cloneid', 'seq_id')\
                                 .replace('ensembl_gene', 'seq_id')] = index # WTF is this?


        #num_lines = len(data); counter = 0
        print len(data[1:])
        for line in data[1:]:
            #print(line)
            #print(header)
            try:
                #print("Trying")
                # For effect size
                ctr_values = []
                exp_values = []

                #counter += 1
                if not line: continue
                columns = line.split('\t')
                if len(columns) < len(header): continue #break #
                seq_id = columns[header['seq_id']]
                symbol = columns[header['symbol']]
                if symbol == "None": symbol = None
                ctr = float(columns[header['ctr']])
                exp = float(columns[header['exp']])
                if "ratio" in header:
                    ratio = float(columns[header['ratio']])
                    if ratio < 1:
                        fold_change = -(1/ratio)
                    else:
                        fold_change = ratio
                else:
                    ratio = float(columns[header['fold_change']]) # 2**exp/2**ctr
                if ratio < 1:
                    fold_change = -(1/ratio)
                else:
                    fold_change = ratio
                # Calculating effect size:
                for k,v  in header.items():
                    if k.startswith('ctr') and k != 'ctr':
                        ctr_values.append(float(columns[v]))
                    elif k.startswith('exp') and k != 'exp':
                        exp_values.append(float(columns[v]))
#                if exp_values and exp_values != ctr_values:
#                    #print exp_values
#                    es = effect_size(exp_values, ctr_values)
#                else:
                es = None
#                if 'pvalue' in header:
#                    pvalue = columns[header['p_value']]
#                else:
                if exp_values != ctr_values:
                    pvalue = t_two_sample(ctr_values, exp_values)[1]
                else: pvalue = 1

                transcript = Transcript(seq_id=seq_id, symbol=symbol, ratio=ratio, fold_change=fold_change, pvalue=pvalue, effect_size=es)

                transcript.save()
                #print(transcript)
                expression = Expression.objects.create(
                    signature=signature,
                    transcript=transcript,
                    exp=exp, ctr=ctr,
                    ratio=ratio,
                    fold_change=fold_change,
                    pvalue=pvalue,
                effect_size=es)
            except ValueError as e:
                print e, symbol, seq_id, fold_change, pvalue, ctr, exp
                #break

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
    num_profiles = Profile.objects.all().count()
    #num_profiles = len(profiles)
    if num_profiles:
        #profiles.delete()
        statement = 'TRUNCATE TABLE expressions_profile'
        cursor = connection.cursor()
        cursor.execute(statement)

        message_type = messages.SUCCESS
    else:
        message_type = messages.WARNING
    msg = "Deleted %s profiles." % num_profiles
    messages.add_message(request, message_type, ugettext(msg))
    return redirect('/expressions/')

@permission_required('is_superuser')
def delete_probes(request):
    statement = 'TRUNCATE TABLE expressions_probe'
    cursor = connection.cursor()
    cursor.execute(statement)
    msg = "Successfully deleted %s probes" % " ".join(cursor.fetchall())
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/expressions/profiles/')

@permission_required('is_superuser')
def delete_replicates(request):
    num_replicates = Replicate.objects.all().count()
    #num_replicates = len(replicates)
    #replicates.delete()
    statement = 'TRUNCATE TABLE expressions_replicate'
    cursor = connection.cursor()
    cursor.execute(statement)
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

@permission_required('is_superuser')
def output_signature(request, pk):
    signature = Signature.objects.get(pk=pk)
    signature.output()
    msg = "Successfully outputted signature: %s" % signature.name
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/expressions/signatures')

def calc_benjamini(signature):
    """Function which preforms the actual Benjamini correction."""
    transcripts = signature.transcripts.all()
    p = [] # seq_id - p-values mapping.
    t = [] #{} # seq_id - transcript mapping.
    for transcript in transcripts.order_by('pvalue'):
        t.append(transcript)
        p.append(transcript.pvalue)
    benjamini_pvalues = calc_benjamini_hochberg_corrections(p, len(p))
    for index, benjamini_pvalue in enumerate(benjamini_pvalues):
        #print  index, benjamini_pvalue
        t[index].benjamini = benjamini_pvalue[1] #expression__
        t[index].save()

def benjamini(request, pk):
    """This view takes a signature and calls a Benjamini Hochberg correction."""
    signature = Signature.objects.get(pk=pk)
    calc_benjamini(signature)
    msg = "Successfully performed Benjamini Hochberg correction on %s" % signature.name
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/expressions/signatures/')

def benjaminis(request):
    "Calls Benjamini Hochberg correction for all signatures in Denigma db."
    signatures = Signature.objects.all()
    for signature in signatures:
        calc_benjamini(signature)
    msg = "Successfully performed Benjamini Hochberg correction on %s" %\
          ", ".join([signature.name for signature in signatures])
    messages.add_message(request, messages.SUCCESS, _(msg))
    return redirect('/expressions/signatures/')

class SetList(ListView):
    queryset = Set.objects.all,
    context_object_name = 'sets',
    template_name = 'expressions/sets.html'
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(SetList, self).get_context_data(**kwargs)
        if hasattr(self, 'extra_context'):
            context.update(self.extra_context)
        context['entry'] = get('Sets')
        return context


class SetCreate(CreateView):
    form_class = SetForm
    model = Set
    template_name = 'expressions/set.html'
    extra_context = {'action': 'Create'}

    def get_context_data(self, **kwargs):
        context = super(SetCreate, self).get_context_data(**kwargs)
        if hasattr(self, 'extra_context'):
            context.update(self.extra_context)
        return context


class ProfileCreate(CreateView):
    context_object_name='profile'
    form_class = ProfileForm
    model = Profile


class SignatureCreate(CreateView):
    form_class = SignatureForm
    model = Signature


# Helper Functions and Classes:
def mean(values):
    return sum(values)/len(values)


class GeneExpressions(dict):

    def recalculate(self):
        for gene in self.values():
            gene.recalculate()

    def benjamini(self):
        genes = self.values()
        p = {}
        for id, gene in genes:
            p[id] = gene.pvalue
        benjamini_pvalues = calc_benjamini_hochberg_corrections(p.values(), len(p))
        for index, in enumerate(benjamini_pvalues):
            gene = genes[index]
            gene.benjamini = benjamini_pvalues[0]
            self[gene.id] = gene


class GeneExpression(object):
    def __init__(self, id, transcript, signature): #exp, ctr, ratio, fold_change, effect_size, pvalue, benjamini):
        expression = Expression.objects.get(transcript=transcript, signature=signature)
        exp=expression.exp,
        ctr=expression.ctr,
        ratio=expression.ratio,
        fold_change=expression.fold_change,
        pvalue=expression.pvalue,
        benjamini=expression.benjamini

        self.id = id
        self.exp = [exp]
        self.ctr = [ctr]
        self.ratio = [ratio]
        self.fold_change = [fold_change]
        self.effect_size = [effect_size]
        self.pvalue = [pvalue]
        self.benjamini = [benjamini]

    def add(self, transcript, signature):
        expression = Expression.objects.get(transcript=transcript, signature=signature)
        exp=expression.exp,
        ctr=expression.ctr,
        ratio=expression.ratio,
        fold_change=expression.fold_change,
        pvalue=expression.pvalue,
        benjamini=expression.benjamini

        self.exp.append(exp)
        self.ctr.append(ctr)
        self.ratio.append(ratio)
        self.fold_change.append(fold_change)
        self.effect_size.append(effect_size)
        self.pvalue.append(pvalue)
        self.benjamini.append(benjamini)

    def recalculate(self):
        self.pvalue = t_two_sample(self.exp, self.ctr)
        self.exp = mean(self.exp)
        self.ctr = mean(self.ctr)
        self.ratio = self.exp/self.ctr

@transaction.commit_on_success
def map_signatures(request):
    print("Initializing mapping.")
    signatures = Signature.objects.all()
    mapped = 0
    total = 0
    for signature in signatures:
        print("Signature: %s" % signature)
        taxid = signature.species.taxid
        transcripts = signature.transcripts.all()
        transcript_count = transcripts.count()
        total += transcript_count
        counter = Counter(transcript_count)
        for transcript in transcripts:
            counter.count()
            gene_id = mapid(str(transcript.seq_id), taxid=taxid)
            if gene_id and isinstance(gene_id, int):
                transcript.entrez_gene_id = gene_id
                transcript.save()
                mapped += 1
            #print transcript, transcript.entrez_gene_id
    msg = "Mapped %s" % (100.*mapped/total)
    messages.add_message(request, messages.INFO, _(msg))
    return redirect('/expressions/signatures/')

@transaction.commit_on_success
def map_signature(request, pk):
    signature = Signature.objects.get(pk=pk)
    taxid = signature.species.taxid
    transcripts = signature.transcripts.all()
    taxid = signature.species.taxid
    mapped = 0
    transcript_count = transcripts.count()
    counter = Counter(transcript_count)

    #geneExpressions = GeneExpressions()

    for transcript in transcripts:
        counter.count()
        gene_id = mapid(transcript.seq_id, taxid=taxid)
        #print transcript, gene_id
        if gene_id and isinstance(gene_id, int):
            transcript.entrez_gene_id = gene_id
            transcript.save()
            #t = Transcript.objects.get(pk = transcript.pk)
            #print("T: %s %s %s" % (t.pk, t.seq_id, t.entrez_gene_id))
            #print transcript, transcript.entrez_gene_id
#        if gene_id:
#            gene, created = Gene.objects.get_or_create(id=gene_id, species_id=taxid)
#            if gene_id not in geneExpressions:
#                geneExpressions[gene_id] = GeneExpression(id, transcript, signature)
#            else:
#                geneExpressions[gene_id].add(transcript, signature)
#            signature.genes.add(gene)
            mapped += 1

    msg = 'Mapped %s' % (100.*mapped/transcript_count)
    messages.add_message(request, messages.INFO, _(msg))
    #genes = signatures.genes.all()

    return redirect('/expressions/signatures/')

#234567891123456789212345678931234567894123456789512345678961234567897123456789