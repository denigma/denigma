from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required

from models import Profile, Signature, Replicate, Set

from views import ProfileCreate, SignatureCreate, SetCreate, SetList

from data import get


urlpatterns = patterns('expressions.views',
    url('^$', 'index', name="expressions"),

    # Profiles:
    url('^profiles/$', login_required('profiles'), name='profiles'),
    url('^profiles/$', # Depricated.
        login_required(ListView.as_view(
            queryset=Profile.objects.all(),
            context_object_name='profiles',
            template_name='expressions/profiles.html')),
        name='expression-profiles'),
    url('^profile/(?P<pk>\d+)', login_required('profile'), name='profile'),
    url('^profile/(?P<pk>\d+)', # Depricated.
        DetailView.as_view(
            model=Replicate,
            context_object_name='profile',
            template_name='expressions/profile.html'),
        name='expression-profile'),
    url('^profile/add/$', login_required('add_profile'), name='add_profile'),
    url('^profile/create/$', login_required(ProfileCreate.as_view()),
        name='create-profile'),
    url('^profiles/delete/$', login_required('delete_profiles'), name='delete_profiles'),

    # Signatures:
    url('^signatures/$', login_required('signatures'), name='signatures'),
    url('^signatures/$', # Depricated.
        login_required(ListView.as_view(
            queryset=Signature.objects.all(),
            context_object_name='signatures',
            template_name='expressions/signatures.html')),
        name='signature'),
    url('^signature/(?P<pk>\d+)', login_required('signature'), name='signature'),
    url('^signature/(?P<pk>\d+)',
        login_required(DetailView.as_view(
            model=Signature,
            context_object_name='signature',
            template_name='expressions/signature.html')),
        name='signature'),
    url('^signature/output/(?P<pk>\d+)', login_required('output_signature'), name='signature-output'),
    url('^signature/create/$', login_required(SignatureCreate.as_view()),
        name='create-signature'),
    url('^signature/add/$',login_required('add_signature'), name='add_signature'),

    url(r'^signature/delete/(?P<pk>\d+)', login_required('delete_signature'), name='delete_signature'),

    url('^signatures/delete/$', login_required('delete_signatures'), name='delete_signatures'),
    url('^signature/benjamini/(?P<pk>\d+)', login_required('benjamini'), name='benjamini'),
    url('^signatures/benjamini/$', login_required('benjaminis'), name='benjaminis'),
    url('^signature/map/(?P<pk>\d+)', login_required('map_signature'), name='map_signature'),
    url('^signatures/map/$', login_required('map_signatures'), name='map_signatures'),
    url('^signature/(?P<name>.+)/$', login_required('signature'), name='signature'),

    # Others:
    url('^replicates/delete/$', login_required('delete_replicates'), name='delete_replicates'),
    url('^transcripts/$', login_required('transcripts'), name='transcripts'),
    url('^transcripts/list/$', login_required('transcript_list'), name='transcript_list'),
    url('^transcripts/delete/$', login_required('delete_transcripts'), name='delete_transcripts'),
    url('^intersections/table/(?P<ratio>[\d\.]+)/(?P<pvalue>[\d\.]+)/(?P<fold_change>[\w\d\.]+)/(?P<exp>[\w\d\.]+)/(?P<set>\d+)/(?P<benjamini>[\w\d\.]+)', login_required('intersections_table'), name='intersection_table'),  # #}
    url('^intersections/$', login_required('intersections'), name='intersections'),
    url('^intersection/(?P<a>\d+)&(?P<another>\d+)/(?P<ratio>[\d\.]+)/(?P<pvalue>[\d\.]+)', login_required('intersection'), name='intersection'),
    url('^meta/', login_required('meta'), name='meta-analysis'),

    # Analysis
    url('^probes/$', login_required('probes'), name='probes'),
    url('^delete_probes/$', login_required('delete_probes'), name='probes'),
    url('^create_signatures/$', login_required('create_signatures'), name='create_signatures'),
    url('^signatures/sets/$', login_required(SetList.as_view(
        queryset=Set.objects.all,
        context_object_name='sets',
        template_name='expressions/sets.html',
        extra_context={'entry': get('sets')})),
    name='sets'),
    url('^signatures/set/create$', login_required(SetCreate.as_view()), name='create-set'),

)
