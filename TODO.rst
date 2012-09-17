======================================
Denigma Enhancement Proposals Protocol
======================================


Denigma Enhancement
===================

These are Denigma Enhancement Proposals (DEPs). 
They are more detailed implementation dietails of the Denigma's Todo list and 
should be written in restructured text. The individual proposal if fully 
applied will become part of the Denigma's documentation. The documentation 
with/and the DEPs (detailed Todos) should should become an app and all the 
follwing entries stored in Denigma db.


Modularity
----------

Small pieces advance quicker. Each app in Denigma is modular and a full 
functional application which can be pluged in into any other project. It can 
have dendencies to other apps, but this need to be programmed in a defense way 
in such that the app is also minimal functional in isolation. The modularity 
of each indiviudal app needs to be guaranted and fully tested.

Modularity should also be applied to every documentation piece asscoiated with 
Denigma, including this document here.


Data app
--------

The Blog and Wiki, Todo as well as associated News and Tutorials and DEPs, 
Documentation app and several otherfollow the same pattern: 
Each one contains an data entry which has a title, a text and tags associated.
tags itself can be data entry or linked to be a data entry. There are further 
meta data associated with each entry such as date of creation (created), 
update (updated). Further images (mutliple) may be associated to an entry of 
which the first one will be the main one. A thumbal view of images must be 
accessible.

Another field might declare whether it is drafted or not, but this is not 
necessary. Each entry content (text) needs to be rendered in html and have 
automatically assigned hyperlinks and should allow to use markup languages. 

It is therefore proposed to have a single data app which eliminates the 
redundance between all this different apps. Either tags or another table maybe 
it can be called type or category declares what type of entry it is. The 
simplest solution is that tags declare also the type of data entry, e.g. 
whether it is a news or tutorial. An immediate implementation of this concept 
was done by using the blog as the data-driving app. The tutorial should 
actually be part of the docs.


Tutorials
---------

The tutorial will be made more comprehensive and functional replace Dengima's 
initial proposal. It needs to include images (maybe later on also videos, etc.) 
and be easily understood even for kids. Actually the tutorials are implemented 
as an app and itself as well as every section in it is fully editable (in line 
with Denigma's core philosophy). However for this route the already present 
admin interface was used, which is suboptimal. Further each app should have 
its on tutorial on how to create it and use it effectively.


Revision Control - north
------------------------

Denigma handles data differently than most common database implementations. 
It provides the possibility that user (actually everyone who verifies her/his 
account) can simply modify the records or even just add additional records,
so it will be possible to maintaining the data integration in a way that scales.

This is actually the whole idea behind Denigma and its philosophy:
Everything is editable an programmable by everyone.

It is anticipated that Denigma can be like a sandbox to try out new ideas and
concepts. It might function as development corner for associated resoures such
as the human aging genomic resources (HAGR). Denigma is perfectly suitable 
for exactly such a purpose.

Of course, there are obstacles in making everything modifyable in Denigma. 
For this reason a  user authentication system was created. Only verified 
users can access all the data structure behind Denigma and makes changes to the 
shape and content of its underlying database which will be tracked back to 
the user and and time of change. In such we don't run in the risk that 
someone corrupts the database. We can just go back and reverse any wrong 
changes.

While south tracks all changes in database schema, The backup app (code name 
north) save/tracks all changes to the content of an app. If a entry gets 
deleted it will be backed up. If the title or content of an entry is changed the 
changes will be saved with associated meta data such as modifing user and time 
of modification. The changes must be able to be visualised so that it is 
possible revisit the history of an entry. 

A lightweight implementation of this concept is django-reversion.

The compatible version of django-revision (1.5.3 for Django-1.3.2) was added to the requirements/project and installed.
django-reversion==1.5.3

::

$ pip install -r requirements/project.txt

Note the latest version reversion-1.6.1 is only compatible with django-1.4.1 but not yet  django-1.5.

Then 'reversion' was added to the INSTALLED_APPS in setting and database synced: ::

$ ./manage.py syncdb

As south was already installed, reversion needed to be migrated: ::

$ ./manage.py migrate reversion

Next revision was integrated with the admin for the respective models.
The required models were simply register with a sublcass of reversion.VersionAdmin: ::

import reversion

class YourModelAdmin(reversion.VersionAdmin):
    pass

admin.site.register(YourModel, YourModelAdmin)

Whenever a model was registered with VersionAdmin the following command needs to be executed: ::

$ ./manage.py createinitialrevisions

This command triggers the population of the version database with an inital set of model data.

Another alternative is django-cutemodel [https://github.com/foxx/django-cutemodel].

Signing up is made simple. All what is required for now is just a user name and 
a password for identifying an individual.



Tracking User Changes
---------------------

The admin history is keept as logs which can be accessed as LogEntry.objects.log_action()
[http://stackoverflow.com/questions/2684980/admin-panel-recent-actions] and enhanced
[http://djangosnippets.org/snippets/1052/].
The Pro Django Book explains an approach how to track changes made by user [http://prodjango.com/].

A simple solution as it was applied in the reference model is to make the 
discriminative fields (i.e. the poperties that determine whether an entry is the 
same) unique (such as pmid and title) but also allow them to be 
blank. A update view and duplicate view was created to manage this.
If more than one field together makes something unique the unique_togethr in the
Meta inner class should be used
[https://docs.djangoproject.com/en/dev/ref/models/options/#unique-together].


Checking if an Entry Already Exists
-----------------------------------

There are several way to check whether an entry already exists and therefore 
prevent duplicate entries. A simple way is to use the helper function
get_or_create() [http://stackoverflow.com/questions/1821176/django-check-whether-an-object-already-exists-before-adding].

To specify behaviour on the creation of a model, overwrite the save() method and
check if self.pk is None, which is the case not yet created entries
[http://stackoverflow.com/questions/2307943/django-overriding-the-model-create-method].

Simplifing Account Creation
---------------------------

User account creation can be even more simplified.
The username should be made optional and only a Email address should be 
required the username will then be infered from the Emial address.
User names actually need to be changeable too.
For known experts the default user name will be assumed to be
FirstName_LastName. Only the Email field is required and password will be
send by email.


Global Site-wide Search
-----------------------

Denigma needs a umnipotent search function which is able to search all fields 
of all tables or only a specified subset as it was similiar implemented in 
Denigma's Wiki.

There are numerous ways on how to implement searching. One option would be 
Haystack/Whoosch and another Xapian/Djapian
[http://www.vlent.nl/weblog/2010/10/14/searching-django-site-part-1-what-and-why/].
For Denigma it was decided to use the former as they are clean pure python implementations.

Haystack and whoosh need to be added to the requirements: ::
    ...
    whoosh
    -e git://github.com/toastdriven/django-haystack.git@master#egg=django-haystack
    ...

Haystack has to be added to the INSTALLED_APPS within the settings.py: ::
    ...
    INSTALLED_APPS = [
        ...
        'haystack',
        ...

Specify the Haystack connections, e.g. for Whoosh: ::
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'), # use PROJECT_ROOT instead of os.path.dirname(__file__)
        }, 
     }


Create search_indexes.py in the corresponding app folder: ::
    import datetime
    from haystack import indexes
    from models import Post


    class PostIndex(indexes.SearchIndex, indexes.Indexable):
        created = indexes.DateTimeField(model_attr='created')
        updated = indexes.DateTimeField(model_attr='updated')

        text = indexes.CharField(document=True, use_template=True)
        tags = indexes.MultiValueField()

        def get_model(self):
            return Post

        def index_queryset(self):
            """Used when the entire index for model is updated."""
            return self.get_model().objects.filter(created__lte=datetime.datetime.now())

An additional file <modelname>_text.txt need to be create in the template directory called
sarch/indexes/myapp/<modelname>_text.txt and the following need to be placed within it:
{{ object.title }}
{{ object.text }}

Add the search view to the URLconf: ::
    ...
    (r'^search/', include('haystack.urls')),
    ...

Lastly reindex by runnig the following command: ::
    $ ./manage.py rebuild_index
 
Unsure that whoosh_index is writeable: ::
    $ chmod 777 whoosh_index

The richard project [https://github.com/willkg/richard] which is used by pyvideo.org
[http://pyvideo.org/search/?models=videos.video&q=django+customizing] is an excellent
example for the implementation of this libraries.

The search template should really be redesigned and perfom a default search. The results
need to be better annotated (e.g. from which model the information stems and in which 
context the term was found.Spell correction and auto-completion should be included.
The global search field should be in grey if not selected and placed more in the centre
of the upper navigation panel.

The rebuild_indexes need to be automated and performed regular.
An alternative real-time search function can be implemented.

Optionally other search engines can be utilized.

Look into the Haystack documentation for more details on implementation way to accomplish
the above proposed enhancement and other functionalities of value
[http://django-haystack.readthedocs.org/en/latest/].


Blog Authors
------------

The block Post should contain the information on which user created it and who updated it and when and what.

The text in the templates should not be static. Rather than they should be saved as database entries under appropiate names in such that they will be editbale in the admin panel.


Dynamic Page Content
--------------------

Information hardcoded in the templates need to be moved into a database-backend and being edidtable
both via the admin interface and directly on the site. These pieces of information need to be made
persistent in either a relational (app) or non-relational (i.e. key-value look-up storage) backend.

One way to accomplish this would be to pass a data object containing all entries of the data app as
dictionary mapping title to entries.

Therefore in the views.py
namespace = [post.title for post in Post.objects.all()]
return render_to_response('appname/templatename.html', {'namepace': namespace})

Although this approach works it produces considerbale overhead as the database will be queried for all
data objects each time the view gets called.

An alternative is to explicilty fetch the required information from data and pass them to the template.

An attractive way to achieve the above mentioning is to use django-constance, which allows to define 
settings constance that are stored in redis backend and already provides an admin interface app for 
editing this constances. settings can be imported into views and passed to templates
[https://github.com/comoga/django-constance].


Literature Retrieval
--------------------

Each referenence should have a link to its full-text article as well as PDF in S3 storage.


Editable Content
----------------

Editable Tables
~~~~~~~~~~~~~~~
Denigma needs to provide a beautiful representation of its table content.
The tables need to be interactive and each row can be editied with DetailView.
Filters can be applyied on and column. A similiar framework to the dynamic 
simulation UI - Data Grid Components has to be employed for this 
[http://nextgensim.info/grids].

Editable Text
~~~~~~~~~~~~~
The Etch content editor need to be utilized [http://etchjs.com/].


Article should be passed to the address bar by their titles.
For this to occur a article title need to be slugfied. A templatetag
could do this job by replacing spaces with other characters.


Tags
----

Denigma currently employs three flavours of tags:
1. Taggit for the Blog posts
2. A simply custom tag for the Wiki
3. A Category tag with optional description for the Links

Those need to be united into a single system.

One possibility is that the data entries (alias blog posts) can themself function
as tags via a ManyToMany field with itself. Further hierarchical relationships
need to be implemented. For this to happen the entries need to provide all the
functionality of taggit, tagging modules.


Automating Schemamigration
-------------------------

South only performs semi-automated schemamigration. It would be usefull to totally
automate this process.

The django-admin-models-editor would provide an excellent starting point as it already
includes a GUI for creating models, generates code for models using HTML forms and 
allows to create models within the admin interface. It is still sub-optimal in the way
it splits the models.py and admin.py. 

It just need to be extended to als edit existing models and integrated with South.
It also need to be extend to cover more field options to deal with things like
"choices".

Database schema defination could also made more graphical with for instance
[http://gaesql.appspot.com/]. 

Another graphical tool runs the other wayL the graph command from django-extensions 
generates UML form Django models [http://code.google.com/p/uml-to-django/].


Tree Menus
----------

For menus django-treemenus enables generic tree-structured menuing system 
[http://code.google.com/p/django-treemenus/].


NoSQL Database
--------------

Denigma needs a powerful NoSQL database-backend
Considered are MongoDB, Neo4j, titan, and orientdb.


Icons
-----
Include icons in the navigation just behind the labels
Take an example from: http://kfalck.net/
<li class="active"><a href="/"><i class="icon-list"></i> Home</a></li>


Visit Counter
-------------
Denigma should be able to count how often its main site as well as individual
parts are visited and keep track of statics on traffic.

django-hitcounts, django-visits-counter or django-visits are attractive ways of
easily implemented such functionality. 


Cross-linking
-------------
Denigma supports mutliple kinds of highly effective automatic cross-linking facilities. The most powerfull is
`recross`, a template tag based on regular expression multi-term replacement.
Individual cross-linking algorithms might be utilized in the views of for instance in the derivates such as
the tutorials. It is also considered to establish a dictionary of important sections in Dengima and use the for
mapping to cross-link also sites which are not direct derivates of the blog posts.
Also explicit cross-links shoul be supported too in order to avoid wrong auto-directing.

The Future of Denigma
---------------------

This is just the beginning. Further DEPs might be:

- Need to get GIT from Denigma server working.
- restore.sh for restoring a snapshotted database.
- Automate EC2 instance setup
  [http://www.turnkeylinux.org/blog/ec2-userdata].
- Use Fabric for ssh control of Denigma 
  [http://docs.fabfile.org/en/1.4.3/index.html].
- Move Denigma db to RDS
- Repair or delete blogs (its broken)
- Candidates is empty, delete it.

May Denigma's future be bright!

#234567891123456789212345678931234567894123456789512345678961234567897123456789
