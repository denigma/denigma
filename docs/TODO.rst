.. footer:: ###Page###

======================================
Denigma Enhancement Proposals Protocol
======================================

.. contents::

Denigma Enhancement
===================

These are Denigma Enhancement Proposals (DEPs). 
They are more detailed implementation details of the Denigma's Todo list and
should be written in restructured text. The individual proposal if fully 
applied will become part of the Denigma's documentation. The documentation 
with/and the DEPs (detailed Todos) should become an app and all the
following entries stored in Denigma db.

Modularity
----------

Small pieces advance quicker. Each app in Denigma is modular and a full
functional application which can be plugged in into any other project. It can
have dependencies to other apps, but this need to be programmed in a defence way in
such that the app is also minimal functional in isolation. The modularity of each
individual app needs to be guaranteed and fully tested.

Modularity should also be applied to every documentation piece associated with
Denigma, including this document here.


Data App
--------


Content is information. Denigma's content is mainly driven by the fundamental Data Unit which is called Data Entry and its associated derivatives the Blog Post and Wiki Pages. Therefore, the data unit comes in three different flavours each one of them with own characteristics an its own specific purpose.

The Data/Entry shall be the most important data unit. The Blog Post will be
a lightweight version of a data unit. While a data entry title has to be
unique the blog posts allow to have multiple units with the same title.
The Wiki/Pages will be kept and be editable even for unregistered users and be
fully in the style of a traditional Wiki, but with many enhancements. The data
app will control the information flow (management and access). Retrieving a data
unit will first query the data entries, then the blog posts and finally the wiki pages.



The wiki shall be freely Editable by everyone.


, which comes in three flavours. The fundamental unit is the data entry,

Tutorials
---------

The tutorial will be made more comprehensive and functional replace Dengima's 
initial proposal. It needs to include images (maybe later on also videos, etc.) 
and be easily understood even for kids. Actually the tutorials are implemented 
as an app and itself as well as every section in it is fully editable (in line 
with Denigma's core philosophy). However for this route the already present 
admin interface was used, which is suboptimal. Further each app should have 
its own tutorial on how to create it and use it effectively.


Revision Control - north
------------------------

Denigma handles data differently than most common database implementations. 
It provides the possibility that user (actually everyone who verifies her/his 
account) can simply modify the records or even just add additional records,
so it will be possible to maintain the data integration in a way that scales.

This is actually the whole idea behind Denigma and its philosophy:
Everything is editable and programmable by everyone.

It is anticipated that Denigma can be like a sandbox to try out new ideas and
concepts. It might function as development corner for associated resources such
as the human aging genomic resources (HAGR). Denigma is perfectly suitable 
for exactly such a purpose.

Of course, there are obstacles in making everything modifyable in Denigma. 
For this reason a  user authentication system was created. Only verified 
users can access all the data structure behind Denigma and make changes to the
shape and content of its underlying database which will be tracked back to 
the user and time of change. In such we don't run in the risk that
someone corrupts the database. We can just go back and reverse any wrong 
changes.

While south tracks all changes in database schema, The backup app (code name 
north) save/tracks all changes to the content of an app. If a entry gets 
deleted it will be backed up. If the title or content of an entry is changed the 
changes will be saved with associated meta data such as modifying user and time
of modification. The changes must be able to be visualised so that it is 
possible to revisit the history of an entry.

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
The required models were simply registered with a subclass of reversion.VersionAdmin: ::

import reversion

class YourModelAdmin(reversion.VersionAdmin):
    pass

admin.site.register(YourModel, YourModelAdmin)

Whenever a model was registered with VersionAdmin the following command needs to be executed: ::

$ ./manage.py createinitialrevisions

This command triggers the population of the version database with an initial set of model data.

Low-level API
~~~~~~~~~~~~~
It is possible to use the version-control outsite the admin.
If a model need to be version-controlled without admin integration it has to be extra
registered: ::

$ nano models.py
$ import reversion
$ reversion.register(ModelName)

Another alternative is django-cutemodel [https://github.com/foxx/django-cutemodel].

Signing up is made simple. All that is required for now is just a user name and
a password for identifying an individual.

There are three possibilities for creating reversions. It is recommended to choose one
and to stick consistently to it.

RevisionMiddleware
^^^^^^^^^^^^^^^^^^
Adding the `RevisonMiddleware` is the simplest way as it automatically warsp every request in a revision and ensueres that all changes will be added to the version history.
It should be preferable used in conjunction and right after `TransactionMiddleware`: ::

    nano settings.py
    ...
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware'
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.transaction.TransactionMiddleware',
        'reversion.middleware.RevisionMiddleware'
        # Other middlewares...
     )

reversion decorator
^^^^^^^^^^^^^^^^^^^
To enable more control over reversion management decorate the function with the `reversion.create_reversion() decorator which groups any change occuring in this function
together into a revision.

    nano views.py
    ...
    import reversion
    ...
    @reversion.create_revision()
    def viewFunction(request):
        model.save()

reversion context manager
^^^^^^^^^^^^^^^^^^^^^^^^^
With the reversion context manager a block of code can be marked for version-control.
After the block terminates the changes made to models will be grouped together into a 
revision: ::

    with reversion.create_reversion():
        model.save()

Version meta data
~~~~~~~~~~~~~~~~~
With the following method it is possible to attach a comment and user reference to an active revision: ::

    with reversion.create_revision():
         model.save()
         reversion.set_user(user)
         reversion.set_comment("Commentary...")

The RevisionMiddleware automatically addes the user to the revision.


Custom meta data
^^^^^^^^^^^^^^^^
Custom meta data can be attached to a revision by creation a separate model to hold the
additional fields. For instance: ::
    nano models.py
    from django.db import models
    from reversion.models import Reversion


    class VersionRating(models.Model):
        revision = models.OneToOneFiel(Revision)  # Required
        rating = models.PositiveIntegerField()

This meta class can be attached to a revision by: ::

    reversion.add_meta(VersionRating, rating=5)


Management Commands
^^^^^^^^^^^^^^^^^^^
The createinitialrevisions commands can be used to create a single, base revision for all registered models,
for all models within an app or for specified models: ::

    django-admin.py createinitialrevisions
    django-admin.py createinitialrevisions someapp
    djanog-admin.py createinitialrevisions someapp.SomeModel


Relationships changes
^^^^^^^^^^^^^^^^^^^^^
Deletion of a study together with a reference, allows to revert the reference but not the study.


django-audit-log keeps track of who changed what model instance. The full model stucture is tracked and kepts in a
seperate table similiar in structure to the original table. Reference to user and time of action as well as the
action indicating it was an insert are also tracked. It actually bootstrap itself in each POST, PUT and DELETE 
request in such it only can track changes that are made vie the web interface
[https://github.com/Atomidata/django-audit-log].


Tracking User Changes
---------------------

The admin history is kept as logs which can be accessed as LogEntry.objects.log_action()
[http://stackoverflow.com/questions/2684980/admin-panel-recent-actions] and enhanced
[http://djangosnippets.org/snippets/1052/].
The Pro Django Book explains an approach how to track changes made by user [http://prodjango.com/]
which was packaged [https://bitbucket.org/q/django-current-user/src].

A simple solution as it was applied in the reference model is to make the 
discriminative fields (i.e. the properties that determine whether an entry is the
same) unique (such as pmid and title) but also allow them to be 
blank. An update view and duplicate view was created to manage this.
If more than one field together makes something unique the unique_togethr in the
Meta inner class should be used
[https://docs.djangoproject.com/en/dev/ref/models/options/#unique-together].

`django-moderation` allows to moderate any model objects where when user create objects or make changes a
moderator must approve it to be visible on the site. It ships admin-integration where data-changes are seen.
It also generates html difference of changes between versions of objects. It supports moderation queue in admin
and configurable email notifications. It also provides custom lde form that allows to edit changed data of object.
Auto approve/reject for selected user groups or user types can be configured. Are major issue is that m2m relations
in models are not currently supported.


Generating Diffs
----------------
django-reversion can generate the differences between revision
[https://github.com/etianen/django-reversion/wiki/Generating-Diffs]
by the use of `google-diff-match-patch` which is
a Diff, Match and Patch Library for plain text
[http://code.google.com/p/google-diff-match-patch/].

The whole diff history of a blog/data post/entry can be viewed by www.denigma.de/meta/diff/<pk>/.


Checking if an Entry Already Exists
-----------------------------------

There are several ways to check whether an entry already exists and therefore
prevent duplicate entries. A simple way is to use the helper function
get_or_create() [http://stackoverflow.com/questions/1821176/django-check-whether-an-object-already-exists-before-adding].

To specify behaviour on the creation of a model, overwrite the save() method and
check if self.pk is None, which is the case not yet created entries
[http://stackoverflow.com/questions/2307943/django-overriding-the-model-create-method].


Check if a Field has Changed
----------------------------
To manually check whether a model field has changed a function in the save method can
be implemented: ::

    def has_changed(instance, save):
        if not instance.pk:
            return False
        old_value = instance.__class__.default_manager.\
                     filter(pk=instance.pk).values(field).get()[field]
        return not getattr(instance, field) == old value

It can be used in the following: ::

    class Entry(models.Model):
        title = ...
        text = ...
        tags = ...
        ...
        def save(self, *args, **kwargs):
            if has_changed(self, 'has_star'):
                # Logi here
            super(Entry, self).save(*args, **kwargs)

An improvement to the above would be to handle files differently as changes in files can have the same
name but different content and comparing different empty values for False: ::

    def has_changed(instance, field):
        if not instance.pk:
            return False
        old_value = instance.__class__._default_manager.\
            filter(pk=instance.pk.values(field).get().get(field, None)
        new_value = getattr(instance, field, None)

        if hasattr(new_value, "file"):
            # Handle FileFields as special cases, beacause the uploaded filename could be
            # the same as the filename that's already there even through there may be
            # different file contents.
            from django.core.files.uploadfile import UploadedFile
            return isinstance(new_value.file, UploadedFile)

        if not (new_value or old_value):
            # Avoid comparing different types of empty values (None, '', {}, [], (), False, etc.)
            # results is False in any case
            return False
         else:
            # in other cases return comparision result as usual
            return not new_value == old_value

So in principle the one way is to check if the value for a field has changed is to fetch the original data from
the database before saving instance: ::

    class Entry(models.Model):
        title = models.CharField(max_length=255):
        ...
        def save(self, *args, **kw):
            if self.pk is not None:
                orig = Entry.objects.get(pk=self.pk)
                if orig.title != self.title:
                    print("Title changed")
            super(Entry, self).save(*args, **kw)

Another attractive alternative way is to override the `__init__` method of the `models.Model` so that it keeps
a copy of the original value. This avoids another DB lookup: ::

    class Entry(models.Model):
        title = models.CharField(max_length=255):
        ...
        __original_name = None

        def __init__(self, *args, **kwargs):
            super(Entry, self).__init__(*args, **kwargs)
            self.__original_name = self.name

        def save(self, force_insert=False, force_update=False):
            if self.name != self.__original_name:
               # name changed - do something here.

        super(Entry, self).save(force_insert, force_update)
        self.__oirignal_name = self.name

The `post_init-signal` can also be used instead of overriding
[https://docs.djangoproject.com/en/dev/ref/signals/#post-init],
but overriding methods is recommended by Django documentation
[https://docs.djangoproject.com/en/dev/topics/db/models/#overriding-predefined-model-methods].

An elegant further option is to use `pre_save` signal: ::

    @reciever(pre_save, sender=Entry):
    def do_something_if_changed(sender, instance, **kwargs):
        try:
            obj = Entry.objects.get(pk=instance.pk)
        except Entry.DoesNotExist:
            pass # Object is new, so field hasn't technically changed,
                 # but maybe something else needs to be done here.
        else:
            if not obj.some_field == instance.some_field: # Field has changed.
                # do something.

The drawback of the latter is that it still involves an extra database hit, but signals are basically used for 
exactly such situations and the method does not require alteration to the model.


Simplifying Account Creation
----------------------------

User account creation can be even more simplified.
The username should be made optional and only a Email address should be 
required, the username will then be inferred from the Email address.
Usernames actually need to be changeable too.
For known experts the default user name will be assumed to be
FirstName_LastName. Only the Email field is required and password will be
sent by email.

Users can be created with an admin method and immediately send the user a "we created a user for you, follow this link
to create a password" email message, where the link is derived from tha admin "reset password" code.

For accomplishing this take a look at: http://github.com/chmarr/artshow-jockey

The relevant function is in artshow/admin.py, ArtistAdmin.create_managment_users()

The link just goes to where the password_reset link would have taken them.

Email as Username
-----------------
Emails can be used as user name. There are several options. An example script is provided 
[http://www.f2finterview.com/web/Django/18/]. The three ways of accomplishing this is: ::

There is an app `django-email-as-username` which allows to treat users as having only
email addresses instead of usernames
[https://github.com/dabapps/django-email-as-username] which is compatible with
django-registration after them considerations [https://github.com/dabapps/django-email-as-username/issues/17].

1.  ALTER statement in the database to make the username longer than 30 chars and design custom
forms that enforce the new field length. Then provide those custom forms to the auth login
views, etc.

2. Fork Django (or at least django.contrib.auth) for the purposes of a local depolyment and
modify the 30 character constraint wherever it occurs.

3. Employ Django 1.5 which will come with the possiblity to allow to install a custom User model
that has whatever properties are desired (e.g. longer username, only an Email fields, twitter handle
instead of username, etc.). The branch is developed here [https://github.com/freakboy3742/django/tree/t3011] 
at will be incorportated in 1.5 [https://docs.djangoproject.com/en/dev/topics/auth/#customizing-the-user-model].

Customization method
~~~~~~~~~~~~~~~~~~~~
First create a backend inside an app called for instance 'accounts': ::

    nano accounts/backends.py
    from django.contrib.auth.backends import ModelBackend
    from django.contrib.auth.models import User


    class EmailBackend(ModelBackend):
        """"A django.contrib.auth backend that authenticates the user
        based on its email address instead of the username."""

        def authenticate(self, email=None, password=None):
            try:
                user = User.objects.get(emai=email)
                if user.check_password(password):
                    return user
                except User.DoesNotExist:
                    return None


Then set the new backend in the Config: ::

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend' # necessary for django.auth
        'accounts.backends.EmailBackend' # Custom backend to authenticate using the email field.
        )

Subsquently modify the login view: ::

    if request.method == 'POST' and unsername and password:
        user = auth.authenticate(username=username, password=password)
        if user is None:
            user = auth.authenticate(email=email, password=password)

Default User
------------
The automatic admin interface of the Django read metadata of models and provides a pwoerful and production-ready
interface that can be utilized by users to add content order to provide the admin interface to the public,
a user account with default password can be created whe the
change password is locked and the credentials are either available publicly or assign to annoymous user automatically.


Global search
-------------
A global search view might list all the installed apps and therein contained models.
The number of hits in each model and app in total should be displayed.
Check-boxes allow to select which apps and models should used for the list of the search results.

Whoosh, lucene, solr are search engines that can be combined with Haystack.

Blog Authors
------------

The block Post should contain the information on which user created it and who updated it and when and what.

The text in the templates should not be static. Rather, they should be saved as database entries under appropiate names in such that they will be editbale in the admin panel.


Dynamic Page Content
--------------------

Information hardcoded in the templates needs to be moved into a database-backend and being editable
both via the admin interface and directly on the site. These pieces of information need to be made
persistent in either a relational (app) or non-relational (i.e. key-value look-up storage) backend.

One way to accomplish this would be to pass a data object containing all entries of the data app as
dictionary mapping title to entries.

Therefore in the views.py
namespace = [post.title for post in Post.objects.all()]
return render_to_response('appname/templatename.html', {'namepace': namespace})

Although this approach works it produces considerbale overhead as the database will be queried for all
data objects each time the view gets called.

An alternative is to explicitly fetch the required information from data and pass them to the template.

An attractive way to achieve the above mentioning is to use django-constance, which allows to define 
settings constance that are stored in redis backend and already provides an admin interface app for 
editing this constances. settings can be imported into views and passed to templates
[https://github.com/comoga/django-constance].


Literature Retrieval
--------------------

Each reference should have a link to its full-text article as well as PDF in S3 storage.


Editable Content
----------------

Editable Tables
~~~~~~~~~~~~~~~
Denigma needs to provide a beautiful representation of its table content.
The tables need to be interactive and each row can be editied with DetailView.
Filters can be applied on and column. A similar framework to the dynamic
simulation UI - Data Grid Components has to be employed for this 
[http://nextgensim.info/grids].

Editable Text
~~~~~~~~~~~~~
The Etch content editor needs to be utilized [http://etchjs.com/].


Article should be passed to the address bar by their titles.
For this to occur an article title needs to be slugfied. A templatetag
could do this job by replacing spaces with other characters.


Tags
----

Denigma currently employs three flavours of tags:
1. Taggit for the Blog posts
2. A simple custom tag for the Wiki
3. A Category tag with optional description for the Links

Those need to be united into a single system.

One possibility is that the data entries (alias blog posts) can themself function
as tags via a ManyToMany field with itself. Further hierarchical relationships
need to be implemented. For this to happen the entries need to provide all the
functionality of taggit, tagging modules.


Automating Schema migration
---------------------------

South only performs semi-automated schema migration. It would be usefull to totally
automate this process.

The django-admin-models-editor would provide an excellent starting point as it already
includes a GUI for creating models, generates code for models using HTML forms and 
allows to create models within the admin interface. It is still sub-optimal in the way
it splits the models.py and admin.py. 

It just need to be extended to als edit existing models and integrated with South.
It also need to be extend to cover more field options to deal with things like
"choices".

Database schema definition could also made more graphical, for instance
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
Denigma supports multiple kinds of highly effective automatic cross-linking facilities. The most powerful is
`recross`, a template tag based on regular expression multi-term replacement.
Individual cross-linking algorithms might be utilized in the views of for instance in the derivatives such as
the tutorials. It is also considered to establish a dictionary of important sections in Dengima and use the for
mapping to cross-link also sites which are not direct derivates of the blog posts.
Also explicit cross-links should be supported too in order to avoid wrong auto-directing.


Media App
---------
The media app will accommodate images, sounds, music, and videos. It will functionally replace the gallery app
and the gallery app itself will be a separate app which uses the media app as data driven backend.


Title too long
--------------
Increasing Saccharomyces cerevisiae stress resistance, through the overactivation of the heat shock response resulting from defects in the Hsp90 chaperone, does not extend replicative life span but can be associated with slower chronological ageing of nondividing cells.

A network biology approach to aging in yeast 
However added Batch Effects and Noise in Microarray Experiments: Sources and Solutions (Wiley Series in Probability and Statistics) 


Request Namespace
-----------------
The current URL name, app name or namespace (or any information gathered
during URL resolution) should be available within views and templates, i.e.
attached to a request.object.

During URL resolution, responses return a ResolveMatch object
[https://github.com/django/django/blob/e72e22e518a730cd28cd68c9374fa79a45e27a9c/django/core/urlresolvers.py#L222;
https://github.com/django/django/blob/e72e22e518a730cd28cd68c9374fa79a45e27a9c/django/core/urlresolvers.py#L331].
ResolveMatch instances have attributes such as app_Name, url_name.
[https://github.com/django/django/blob/e72e22e518a730cd28cd68c9374fa79a45e27a9c/django/core/urlresolvers.py#L39]

HTTP handlers manage both the URL resolution and the request object.
They could assign url_name or app_name to request [https://github.com/django/django/blob/e72e22e518a730cd28cd68c9374fa79a45e27a9c/django/core/handlers/base.py#L104 
].

Changing in [https://github.com/django/django/blob/e72e22e518a730cd28cd68c9374fa79a45e27a9c/django/core/handlers/base.py#L104]

    callback, callback_args, callback_kwargs = resolver.resolve(request.path_info)

into: ::

    request.resolver_match = resolver.resolve(request.path_info)
    callback, callback_args, callback_kwargs = request.resolver_match

Then in template it would be possible:

    <a href="{% url foo %} {% if request.resolver_match.url_name == 'foo' %}calss="active"{% endif %}>Foo</a>

In a nutshell ResolveMatch needs to be saved in HttpRequest:
    https://code.djangoproject.com/ticket/15695

A small test that illustrates what is needed to accomplish this is available as
django-locale-switcher [https://github.com/apollo13/django-locale-switcher].
This app stuffes the resolver_math on the request.


Filtering
---------
Tables in Denigma need to be filtered dynamically also in the public interface
just as it is accomplished in the admin.
`django-filters` allows user to filter queryset dynamically 
[https://github.com/alex/django-filter].


Adding Many-To-Many Relationships in bulk
-----------------------------------------
To add a bulk of many-to-many relationships the `bulk_create` can be used. 
For this a list of B objects is first created in bulk and then added them all at once to the
ManyToMany relationship of A instance(s): ::

    class A(models.Model):
        b = models.ManyToManyField('B')

    class B(models.Model):
        # fields

    entries = [
        B(...),
        B(...),
        B(...),
        ...
    ]

    B.objects.bulk_create(entries)
    a.b.add(*o)


Multiple File Upload
--------------------
It would be of interest to enable upload of multiple files simultaneously.
`django-multiple-file-uploads` provides exactly this feature 
[http://www.chicagodjango.com/blog/multiple-file-uploads-django/].


Compound static-dynamic pages
-----------------------------
To reduce repetition of static components they need to be made dynamic.
A solution would be the following: [http://dpaste.com/hold/806276/].


Dynamic Sections links
----------------------
The tutorials app should have a dynamic sections links navigation as it is
implemented in the bootstrap getting started [http://twitter.github.com/bootstrap/getting-started.html].


Notifications
-------------
django-notifications-hq provides GitHub notifications alike app for Django: [http://pypi.python.org/pypi/django-notifications-hq]


Speeding up Django
------------------
Django performance in web framwork and template enigine can be drastically improved by employing Pypy 1.9
(vs. CPython 2.7):
http://mindref.blogspot.de/2012/09/python-fastest-web-framework.html
http://mindref.blogspot.de/2012/07/python-fastest-template.html

The source code of the benchmarking hello world app is available
[https://bitbucket.org/akorn/helloworld/src].


Use Buildout to Deploy
----------------------
zc.buildout allows to perform more complex tasks than just installing applications
in the virtualenv as pip does [http://jacobian.org/writing/django-apps-with-buildout/;
[http://pypi.python.org/pypi/zc.buildout].

URL import from future
----------------------
Need to prepare the URLs to make them compatible with Django-1.5.


Preview
-------
Enable a preview for all form submissions. Django provides FormPreview_ for this purpose.
data entry require a real time previews.
`Realtime preview of markdown`_ forms was asked on stackedoverflow.
django-pagedown_ is the way to go

.. _FormPreview: https://docs.djangoproject.com/en/dev/ref/contrib/formtools/form-preview/
.. _`Realtime preview of markdown: http://stackoverflow.com/questions/12137459/is-there-any-django-app-for-realtime-preview-of-markdown
.. _django-pagedown: https://github.com/timmyomahony/django-pagedown


Formatting Instruction
----------------------
Write formatting instruction for Data/Entry Blog/Post usage.
Such as: ::

    Format using Markdown/ReStructuredText (No HTML if possible)
    * Code block: prefix each line by at least 4 spaces or 1 tab (and a blank line before and after)
    * Code span: surround with backticks
    * Blockquotes: prefix lines to be quoted with >
    * Links: <URL>
    * Links w/ descriptions: [description](URL)


Markup
------
The rendered value of the data entry text field can be cached on the assumption that disk space is cheaper than CPU
cycles in a web application (See django-markupfield).

`Semi-automatic reST table generation`_ might be implemented with javascripting.

.. _ `Semi-automatic reST table generation`: http://vimeo.com/14300874

reST Rich-text editor
---------------------
Widgets can be enabled to render a form field as a TinymCE editor (django-tinymce_).
There are also ``RichTextField`` and ``CKEEditorWidget`` utilizing CKEditor availbale
(django-ckeditor_), with image and browsing support included.

.. _django-tinymce: https://github.com/aljosa/django-tinymce
.. _django-ckeditor: https://github.com/shaunsephton/django-ckeditor

A rich text editor might be employed for editing rst data entries (`rst2pdf.net`_)

.. _`rst2pdf.net`: http://www.rst2pdf.net/

Code Highlighting
-----------------
Pygments can be implemented to colorful highlight code syntax.
Synthax highlighting can be easily added to reST (code-highlighting-with-rest_).
The sourcecode or code-block directive can bus used for this. Also sphinx can
do highlighting (syntax-highlighting-for-code_).

.. _code-highlighting-with-rest: http://stefan.sofa-rockers.org/2010/01/13/django-highlighting-rest-using-pygments/
.. _syntax-highlighting-for-code: http://python.6.n6.nabble.com/Syntax-highlighting-for-code-examples-on-PyPI-td1972284.html

Secruity
--------
fail2ban prevents automatic password hacking.

IP Address Blocking
------------------
Bad IP addresses can be blocked automatically
[https://groups.google.com/forum/?fromgroups=#!topic/django-users/4dlo6p2QHRw].

Alterantive Deployment
----------------------
Dengima could be run on OpenShift_ or on Heroku_.

.. _OpenShift: https://openshift.redhat.com/community/get-started/django
.. _Heroku: https://devcenter.heroku.com/articles/django

Dengima Sphere
--------------
The Spehere representing Denigma shall be in red. On its surface there you can see reflection of either the
binary code (010101), asiatic symbols in matrix style or the four bases which make up the genetic code,
depending on which mode Denigma is currently in (in blue, violette or green).


Multiple Databases
==================
Multi-DB --> Postgres, MongoDB

Postgres
--------
The choice between RDS/MySQL and Postgres depends on the
`scalability & load requirements`_.
For high load and high scalability MySQL might be more efficient.

`MySQL to PostgreSQL migration` might be troublesome.

A `migration from MySQL to PostgreSQL`_ is possible thanks
to Django ORM and multiple database support. Django's
serializers move the data from MySQL's format into JSON
and the back into Postgres.

.. _ `scalability & load requirements`: http://stackoverflow.com/questions/8869858/amazon-rds-mysql-vs-postgresql-on-ec2-ebs
.. _`MySQL to PostgreSQL migration`: http://stackoverflow.com/questions/17717/migrating-from-mysql-to-postgresql
.. _migration from MySQL to PostgreSQL`: http://www.ofbrooklyn.com/2010/07/18/migrating-django-mysql-postgresql-easy-way/

Genesis
=======
The Genesis project is about creating artificial life. What are the preqiste for life?
There only three requirements:

1. Replication
2. Variation
3. Selection

The intention is to generate a program that can replicate itself and by
doing it changing its own code with each replication.
Replicates that are defective or inefficient are eliminated.

EVA
===
The EVA project will construct a artifical intellegent. The akrynom EVA stands for Electronic Video Assistent.
EVA is a research interface on the top of a massive database (Denigma) that was first conceived in the Second World War,
and slowly develops into a pseudo-AI. Its primarily role is coordinating and processing information, research progress
and status and providing scientists, programmers as well as designer with a versatile and powerful command tool,
 using the appropiate python files (eva_).

 .. _eva: http://cnc.wikia.com/wiki/Electronic_Video_Agent

EVA sound files [http://www.commandandconquer.com/forums/archive/index.php/t-381.html].

Denigma secret function is to hype aging research.

The Singularity gives us hope. It makes us stronger. Believing in the future.
Do not look back, head on!

Handling Billions of Rows
=========================
It is possible to handle a MySQL InnoDB table on EC2 with more than one billion of rows
and a size about 160 Gb (billion-row-database_).
For instance creating indexes AFTER importing data is generally the fastest approach,
but there is not automated tool for that.

.. _billion-row-database: http://blog.simplicitymedialtd.co.uk/?p=225

Textarea with numbered lines
============================
Through the use of javascript its posssible to add line numbers to a textarea (linenumbers_).

.. _linenumbers: http://www.dhtmlgoodies.com/forum/viewtopic.php?t=506

Database Synchronization
========================
A Denigma Unit must be capable of synchronization with the main one.
Differences can be either in the content, on the code base, or
media. Code base differences will be merged via GIT. Content and
media should theoretically be synchronizable via a fast internet
connection.

Thumbnails
==========
See post on django-user mailing list: `thumbnail image from original on the fly without using a model field?`
An inclusion of pre-build Thumbinal solution as Django Contribution is in discussion
[https://code.djangoproject.com/wiki/ThumbNails].

Countdown
=========
A countdown need to be placed which depict the time
left until Denigma will be made public.

Sign Up Username Check
======================
Simple Ajax that tries to know whether the username already exist before registering.

.. sourceode:: javascript

    # template.html
    function checkUserNameUnique() {
        $.ajax({url:"/ajax/",
            data:{username:$("input.username").val()},
            success: function(result){
                $("span#usernameMessage").text(result);
            }
        }
        );
    }

.. soucecode:: python

    # view.py
    def ajax(request):
        username = request.GET["username"]
        msg = ""
        try:
            user = User.objects.get(username=username)
            msg = "username already exists"
        except User.DoesNotExist:
            msg = "username is okay"
        return HttpResponse(msg);



Multiprocessing
---------------

Monitoring
----------
Graphite is an enterprise-scale monitoring tool that runs well on cheap hardware
[http://graphite.wikidot.com/]. It does two things:

1. Store numeric time-series data
2. Renders graphs of thei data on demand

"Pro python system administration" by Rytis Sileika covers monitoring.
Jinja2 is used for generating template, but it is also possible to use
django for this task.

Audio
=====
django-audiotracks [http://pypi.python.org/pypi/django-audiotracks/0.2.1]
mumble-django [http://www.mumble-django.org/docs/en].


Calender
========


DateTime Picker
===============
Enable to display columns that are of date-time format with some kind of calender picker.
For instance check out bootstrap-datepicker which at least allows to pick date but not time.

Social Networks
===============
django-allauth enables 3th party (social) authentication [https://github.com/pennersr/django-allauth].

The Future of Denigma
---------------------

This is just the beginning. Further DEPs might be:

- Need to get GIT from Denigma server working. Check out django-gitana [https://github.com/lubico-business/django-gitana].
- restore.sh for restoring a snapshotted database.
- Automate EC2 instance setup
  [http://www.turnkeylinux.org/blog/ec2-userdata].
- Move Denigma db to RDS
- Repair or delete blogs (its broken)
- Candidates is empty, delete it.

May Denigma's future be bright!


Customer Relationship Management
================================
A CRM is a model for managing interactions with current and future customers.
It uses technology to organize, automate and synchronize, sales, marketing, customer service, and technical support.
koalixcrm is [www.koalix.org; https://github.com/scaphilo/koalixcrm] provides these functionalities.
There is an english and german demo of koalixm [http://demokoalixcrm.koalix.org/admin/; http://germandemokoalixcrm.koalix.org/admin/].

Email
=====
Lamson Project is an Email server written in Python that adopts modern web application framework design
[http://lamsonproject.org].
It got an API that makes it easy to set up triggers/filters when mails arrives

Online Shop
===========
There are plenty of FLOSS frameworks and apps written for online shops (i.e. ecommerce).
[http://www.satchmoproject.com/; https://www.django-shop.org/ecosystem/].

Django Book
===========
The django book has been open-sourced [https://github.com/jacobian/djangobook.com].

Tag Groups
==========
django-mptt allows to define tag groups.

.. sourcode:: python

    class Tag(models.Model):
        name = models.CharField(max_length=50, unique=True, db_index=True)
        parent = models.ForeignKet('self', null=True, blank=True, related_name='children')

        def __unicode__(self):
            if self.parent: return '%s%s' % ('-', self.name)
            return self.name


    class AlbumAdminForm(forms.ModelForm):
        class Meta:
            model = Album
        tags = forms.ModelMultipleChoiceField(queryset=getqueryset(), required=False,
            widget = FilteredSleect

COM
===
The Com sector is the communication system on Denigma.
It provides a lightweight chat application, a pastebin app, as well as a full-blown
messaging system.

Com

- chat
- pastebin
- messaging
- videochat


Django + jQuery = Ajax Chat [http://vimeo.com/4902952].
evserver-chat [http://www.youtube.com/watch?v=gl3opNjN1Aw].

Management System
=================
Tree.io is an all-inclusive cloud-based business management system
[http://tree.io/en/tour; https://github.com/treeio/treeio].
Django-messaging with threaded messaging [django-threaded-messages].

Tree Widget
===========
Trees can be constructed dynamically via Javascript
[http://www.jstree.com/;
https://github.com/bombino/jquery-tree-select;
http://code.google.com/p/jquery-option-tree/]

User'sessions
=============
By default it is not possible to find an user's session from an user's id.
Sessions are not always associated to users.
However, modifying the django_session table to add an explicit user_id can make life
a lot easier [http://stackoverflow.com/a/4892370/938046].

File Upload
===========
Upload Multiple Files Using Ajax [http://malsup.com/jquery/form/].
There is an app to provide such functionality [https://github.com/blueimp/jQuery-File-Upload].

All Objects related to a User
=============================
In projects with multiple apps is is often useful to get all objects related to a
particular user using the contentTypeFramework.
The following methods enables such queries:

.. sourcode:: python

    User._meta.get_all_related_m2m_objects_with_model()
    User._meta_get_all_related_objects()
    User._meta.get_all_related_many_to_many_objects()
    User._meta.get_all_related_objects_with_model()

Where get_all_related_objects() is the one that has the most common usage.

For example to get all the related objects of a user objects:

.. sourcecode:: python

    # Get a list of attribute names for each related object to an user:
    # e.g. ['logentry_set', 'api_key', 'userprofile_set', 'recipient_set', 'customer']
    user = User.objects.get(username="hevok")
    related_links = [rel.get_accessor_name() for rel in
                     user._meta.get_all_related_objects()]

    # Iterate over this list:
    for link in related_links:
        objects = getattr(user, link.all())
        for object in objects:
            # Do something with object:
            print object

Whereby, getattr(user, link) is the manager for that relate object.



Bookmarks
=========
Bookmark apps:

* [https://github.com/brosner/django-bookmarks]
* [https://github.com/raynesax/django-bookmarks]
* [http://django-generic-bookmarks.readthedocs.org/en/latest/]

If the text and title for an url need to be extracted [http://viewtext.org/help/api].

Automated Deployment
====================
Use Fabric for ssh control of Denigma [http://docs.fabfile.org/en/1.4.3/index.html].
Consider Ansible, puppet and chef for automation with version control.

To prevent python-mysqldb error, install python-mysqldb from apt-get::

    sudo apt-get install python-mysqldb

Then use system packages where available with::

    virtualenv env --system-site-packages

This install mysqldb from apt, which should generally work better with
the version, etc. on the machine that the one installed from pip.

The fabfile.py of the Mezzanine CMS Project is a a complete example to on how to
deploy automatically django project that use nginx, gunicorn and supervisord
[https://github.com/stephenmcd/mezzanine/blob/master/mezzanine/project_template/fabfile.py].

Automated collect static update
-------------------------------
echo yes | ./manage.py collectstatic


Resize image
============
djanog-imagekit
sorl-thumbnail provides thumbnail for Django, totally rewritten
[https://github.com/sorl/sorl-thumbnail].

get_absolute_url With Custom Extra Parameter
=============================================

.. sourcecode:: python

    def _get_absolute_url(self, view='t'):
        return reverse('show_album', args=[view, str(self.id)]) + self.url

    def get_absolute_url_f(self)
        return self._get_absolute_url('f')

    def get_absolute_url_t(self):
        return self._get_absolute_url('t')

    def get_absolute_url(self):
        return self._get_absolute_url()



Autocompletion
==============
Enable autocompletion for fields where it makes sense:
[https://github.com/yourlabs/django-autocomplete-light]

Migrating to Custom User
========================
South can be used to migrate an existing auth.User to Django 1.5. Custom User table:

1. Add 'custom' user model that has exactly the same fields as the current user model.
2. Add a schema migration to rename auth_user to the new required table name.
3. Run the migration.
4. Modify the user model as you see fit.
5. Generate schema migrations as per any other model.


#234567891123456789212345678931234567894123456789512345678961234567897123456789