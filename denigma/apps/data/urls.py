from django.conf.urls import patterns, url
from django.views.generic import  ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from models import Entry, Change, Relation, Alteration, Tag
from views import EntryList, ChangeList, EntryCreate, EntryUpdate, RelationCreate, RelationUpdate


urlpatterns = patterns('data.views',
    url(r'^$', 'index', name='data'),

    # Entries:
    ## Class-Views
    url(r'^entries/list/$', EntryList.as_view(paginate_by=10), name='list-entries'),
    url(r'^entry/table/$', EntryList.as_view(template_name='data/entry_table.html'), name='entry-table'),
    url(r'^hierarchy/list/$', EntryList.as_view(
            context_object_name='entries',
            template_name='data/hierarchy.html'),
        name='list-hierarchy'),
    url(r'^entry/(?P<pk>\d+)', DetailView.as_view(model=Entry), # template_name='entry_detail.html' # use defaults
        name='detail-entry'), # User generic class-based view
    url(r'^entry/create/$', EntryCreate.as_view(), name='create-entry'),
    url(r'^entry/update/(?P<pk>\d+)', EntryUpdate.as_view(),
        name='update-entry'),
    url(r'^entry/delete/(?P<pk>\d+)', DeleteView.as_view(model=Entry),
        name='delete-entry'),

    ## Function-Views:
    url(r'^entries/$', 'entries', name='entries'),
    url(r'^hierarchy/$', 'hierarchy', name='hierarchy'),
    url(r'^entry/(?P<slug>.+)', 'entry', name='data_entry'), # Classic view.
    url(r'^entry/add', 'add_entry', name='add_entry'),
    url(r'^entry/edit', 'edit_entry', name='edit_view'),
    url(r'^entry/remove', 'remove_entry', name='remove_entry'),

    # Changes:
    ## Class-Views
    url(r'^changes/list/$', ListView.as_view(
            queryset=Change.objects.filter(of__published=True).order_by('-at'),
            paginate_by=30),
        name='list-changes'),
    url(r'^change/details/(?P<pk>\d+)', DetailView.as_view(model=Change), name='detail-change'), #detail-change
    url(r'^change/delete/(?P<pk>\d+)', DeleteView.as_view(model=Change), name='delete-change'),
    ## Function-Views:
    url(r'^changes/(?P<pk>\d*)', 'changes', name='changes'),
    url(r'^change/remove/(?P<slug>.+)/$', 'remove_change', name='remove_change'),
    url(r'^change/(?P<slug>.+)/$', 'change', name='change'),


    # Relations:
    ## Class-Views
    url(r'^relations/list', ListView.as_view(queryset=Relation.objects.all()), name='list-relations'),
    url(r'^relation/(?P<pk>\d+)', DetailView.as_view(model=Relation), name='relation-details'),
    url(r'^relation/create', RelationCreate.as_view(), name='create-relation'),
    url(r'^relation/update/(?P<pk>\d+)', RelationUpdate.as_view(), name='update-relation'),
    url(r'^relation/delete', DeleteView.as_view(model=Relation), name='delete-relation'),
    ## Function-Views:
    url(r'^relations/$', 'relations', name='relations'),
    url(r'^relation/(?P<slug>.+)', 'relation', name='relation'),
    url(r'^relation/add/$', 'add_relation', name='add_relation'),
    url(r'^relation/edit', 'edit_relation', name='edit_relation'),
    url(r'^relation/remove', 'remove_relation', name='remove_relation'),

    # Alterations:
    ## Class-Views
    url(r'^alterations/list/$', ListView.as_view(queryset=Alteration.objects.all().order_by('-at')), name='list-alterations'),
    url(r'^alteration/(?P<pk>\d+)', DetailView.as_view(model=Alteration), name='detail-alteration'),
    ## Function-Views
    url(r'^alterations/$', 'alterations', name='alterations'),
    url(r'^alteration/(?P<slug>d+)', 'alteration', name='alteration'),

    # Tags/Categories:
    ## Class-Views
    url(r'^tags/list/$', ListView.as_view(queryset=Tag.objects.all()), name='list-entry-tags'), # Shows number of tagged entries.
    url(r'^tag/(?P<pk>\d+)', DetailView.as_view(model=Tag), name='entry-tag-detail'), # Shows list of tagged entries.
    ## Function-Views
    url(r'^tags/$', 'tags', name='entry-tags'),
    url(r'^tag/(?P<slug>.+)', 'tag', name='entry-tag'),

    #url(r'^')

)#234567891123456789212345678931234567894123456789512345678961234567897123456789