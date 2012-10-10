from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from models import Profile, Signature, Replicate, Set

from views import ProfileCreate, SignatureCreate, SetCreate, SetList

from data import get


urlpatterns = patterns('expressions.views',
    url('^$', 'index'),

    # Profiles:
    url('^profiles/$', 'profiles', name='profiles'),
    url('^profiles/$', # Depricated.
        ListView.as_view(
            queryset=Profile.objects.all(),
            context_object_name='profiles',
            template_name='expressions/profiles.html'),
        name='expression-profiles'),
    url('^profile/(?P<pk>\d+)', 'profile', name='profile'),
    url('^profile/(?P<pk>\d+)', # Depricated.
        DetailView.as_view(
            model=Replicate,
            context_object_name='profile',
            template_name='expressions/profile.html'),
        name='expression-profile'),
    url('^profile/add/$', 'add_profile', name='add_profile'),
    url('^profile/create/$', login_required(ProfileCreate.as_view()),
        name='create-profile'),
    url('^profiles/delete/$', 'delete_profiles', name='delete_profiles'),

    # Signatures:
    url('^signatures/$', 'signatures', name='signatures'),
    url('^signatures/$', # Depricated.
         ListView.as_view(
            queryset=Signature.objects.all(),
            context_object_name='signatures',
            template_name='expressions/signatures.html'),
        name='signature'),
    url('^signature/(?P<pk>\d+)', 'signature', name='signature'),
    url('^signature/(?P<pk>\d+)',
        DetailView.as_view(
            model=Signature,
            context_object_name='signature',
            template_name='expressions/signature.html'),
        name='signature'),
    url('^signature/output/(?P<pk>\d+)', 'output_signature', name='signature-output'),
    url('^signature/create/$', login_required(SignatureCreate.as_view()),
        name='create-signature'),
    url('^signature/add/$','add_signature', name='add_signature'),

    url(r'^signature/delete/(?P<pk>\d+)', 'delete_signature', name='delete_signature'),

    url('^signatures/delete/$', 'delete_signatures', name='delete_signatures'),
    url('^signature/benjamini/(?P<pk>\d+)', 'benjamini', name='benjamini'),
    url('^signatures/benjamini/$', 'benjaminis', name='benjaminis'),
    url('^signature/map/(?P<pk>\d+)', 'map_signature', name='map_signature'),
    url('^signatures/map/$', 'map_signatures', name='map_signatures'),

    # Others:
    url('^replicates/delete/$', 'delete_replicates', name='delete_replicates'),
    url('^transcripts/$', 'transcripts', name='transcripts'),
    url('^transcripts/list/$', 'transcript_list', name='transcript_list'),
    url('^transcripts/delete/$', 'delete_transcripts', name='delete_transcripts'),
    url('^intersections/$', 'intersections', name='intersections'),
    url('^intersection/(?P<a>\d+)&(?P<another>\d+)/(?P<ratio>[\d\.]+)/(?P<pvalue>[\d\.]+)', 'intersection', name='intersection'),
    url('^meta/', 'meta', name='meta-analysis'),

    # Analysis
    url('^probes/$', 'probes', name='probes'),
    url('^delete_probes/$', 'delete_probes', name='probes'),
    url('^create_signatures/$', 'create_signatures', name='create_signatures'),
    url('^signatures/sets/$', SetList.as_view(
        queryset=Set.objects.all,
        context_object_name='sets',
        template_name='expressions/sets.html',
        extra_context={'entry': get('sets')})),
    url('^signatures/set/create$', login_required(SetCreate.as_view()), name='create-set'),

)
