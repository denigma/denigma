.. header::
   Main Doc - page ###Page###

.. footer::
   ###Page###

=====================
Denigma Documentation
=====================

:Abstract: Denigma is not just a Engima which starts with D, the Denigma 
    project is a DDD (Documentation-Driven Development). Its source code is 
    documented from the very beginning. Every decision is documented as well as 
    every issue encountered including the corresponding found solution to it. 
    In contrast to papers and reviews, in Denigma *the ink is never dry*. It 
    changes continuously until it gets it absolutely right.

.. contents::

.. raw:: pdf

   PageBreak oneColumn

Deploying Denigma
=================

To deploy Denigma in the clouds the Amazone Web Service (AWS) is used.

1. Launch an Ubuntu AMI:

   In the past a maverick build such as the ami-975a6de3 (called Giter; which
   ships a GIT repository) or the ami-fd7b4089 (called Daily which is
   up-to-date and does not require updating/upgrading or more precise minimal 
   updating/upgrading) was preferable. However due to updates the use the
   Ubuntu Cloud Guest AMI ID ami-c1aaabb5 (called Ami which ships Ubuntu 12.04 LTS) is highly
   recommended

   Set up of Giter took approximately several minutes and the
   Daily took a little less bit due to the already installed updates (However the
   inclusion of additional third-party libraries increased this time significantly).

   The set up of an Ami takes some time.

2. Create and mount an separate EBS Volume to it.

3. ssh into the machine with the DNS and keypairs acquired from the Amazone
   Control Center (use bash ami.sh). On the machine::

   $ sudo su
   $ cd ..
   $ aptitude install git # Only on Daily, not necessary on Giter. 
   $ git clone https://github.com/hevok/denigma
   $ bash denigma/configure.sh

Where <DNS> is the that of the instance that hast the database and <PASSOWRD> is the password
of the database is there is any.

Serving Media
=============

The media/static files for the Admin Interface were intially not used and there
it was unstyled. To solve this issue:

1. Add the following line to the Apache config file (/etc/apache2/http.conf):

   Alias /django/contrib/admin/media/ /home/denigma/env/lib/python2.6/site-packages/django/contrib/admin/media/

2. Set in the settings.py:

   ADMIN_MEDIA_PREFIX = '/django/contrib/admin/media/'

Similar Pinax static files were also not used right after deploying.
Copying of the static files from the pinax_theme_botstrat/static/ into project/site/media solved this problem: ::

$ cp -rf /home/denigma/env/lib/python2.6/site-packages/pinax_theme_bootstrap/static/. /home/denigma/denigma/media

However removing this files again does not abolish the styling, immediatly 
but with some delay. Possible the cookies forget about it or something (reload 
cookies with Ctrl + F5).


'bool' object has no attribute 'status code'
============================================

It appears that the pinax.middleware.security.HideSensitiveFieldsMiddleware in 
the MIDDLEWARE_CLASSES of the settings.py is causing an error which propagates 
and makes debuging nearly impossible
[http://comments.gmane.org/gmane.comp.python.django.pinax.devel/104].

Deactivating it by commenting out abrogates this problem. Consider to inlcude 
it with an if statement only in debuging mode.


Missing Markup
==============

In the Wiki view.html the load markup tag raised an error. Including the 
"django.conrib.markup" in the settings.py fixed it 
[http://stackoverflow.com/questions/6399649/django-markup-templatetags-error].


CSRF Problem
============

Submit forms such as those in the Wiki edit and search need to be tagged with a
{% csrf_token %}. This worked fine for the edit form 
[findhttp://jordanmessina.com/2010/05/24/django-1-2-csrf-verification-failed/]. 
However it failed on the search form. Deactivating by commenting out the django.middleware.csrf.CsrfViewMiddleware in the MIDDLEWARE_CLASSES resolved 
this problem, but is only a suboptimal solution. Adding a RequestContext 
handler to the render_to_response in the search view which was already present 
in the edit view resolved this issue 
[http://stackoverflow.com/questions/3197321/csrf-error-in-django].
15186745

mysql in virtual env 
====================

For interfacing with mysql of the purpose of database evolution 
libmysqlclient16-dev library is required 
[http://stackoverflow.com/questions/8868545/installing-mysql-for-python-within-virtual-environment].
Note that the Ubuntu 12.04 repository does not contain these specific library 
anymore, but rather that provides libmysqlclient-dev 
[http://askubuntu.com/questions/137788/problem-with-deleting-libmysqlclient16-dev-from-repository-of-12-04].

::

$ aptitude install libmysqlclient16-dev

$ pip install MySQL-python

Depricated Constants
====================

Runnig python denigma/manage.py migrate --list just returns that ENGINE is 
depriciated [http://jira.osqa.net/browse/OSQA-712].


mysql-ebs
=========
 
Prepare db for snapshot::

$ mysql -u root
$ FLUSH TABLES WITH READ LOCK;
$ SHOW MASTER STATUS;
$ SYSTEM sudo xfs_freeze -f /vol


Create Snapshot::

$ SYSTEM sudo xfs_freeze -u /vol
$ UNLOCK TABLES; # Release lock.
$ EXIT


Clean up::

$ sudo /etc/init.d/mysql stop
$ sudo umount /etc/mysql /var/lib/mysql /var/log/mysql /vol


Restoring a snapshotted database
================================

::

$ cd ..
$ sudo su
$ aptitude install git
$ git clone https://github.com/hevok/denigma
$ bash denigma/reconnect-ebs.sh
$ bash denigma/open-port.sh
$ sudo bash ./denigma/aws-django -n denigma -d nothing -s "/s" -H <DNS> -D denigma -U denigma -P <PASSWORD>

ec2-54-246-29-195.eu-west-1.compute.amazonaws.com

Transferring data onto EC2
==========================

It is considered to transfer the Denigma database directly onto an EC2 
instance. SFTP (secruity file transfer protocol) can be used via port 22 to 
directly exchange data with the EC2 instance. FileZilla can be used for this 
purpose [http://www.turnkeylinux.org/forum/support/20100413/how-do-you-get-data-and-out-ec2].
Add the keypair via settings [http://www.codestore.net/store.nsf/unid/BLOG-20111012-0812].
Settings in Ubuntu are at the terminal bar 
[http://superuser.com/questions/159846/change-filezilla-settings-in-ubuntu-linux-so-view-edit-uses-gedit].
Convert the keypair from .pem to .pkk 
[http://www.onebloke.com/2011/06/filezilla-sftp-and-amazon-ec2/].

::

$ sudo aptitude install filezilla

> Open the Site Manage
Host: <DNS>
Port: 22
Logon Type: Normal
User: Ubuntu 

> Edit > Settings
SFTP > Add keyfile...
Convert key

It is noted that when FileZilla transferes data to a EC2 instance it results 
into a block of the internet connection. Possible another port such as 21 has 
to be preferred for connecting to an EC2 instance via sFTP.


Customizing Django Admin
========================

Creating a admin folder in project template directory and modifying the 
original admin templates in this folder allows to do basic customization of the
admin interface. In this way for instance the title can be changed 
[http://overtag.dk/wordpress/2010/04/changing-the-django-admin-site-title/].


App Renaming
============
A entire app can be renamed and the south migration history can be preserved by
performing defined steps [http://stackoverflow.com/questions/4566978/renaming-an-app-with-django-and-south;
https://github.com/ASKBOT/django-south-app-rename-example/commit/f7f2218af612922416b4164adae589e86de19951

Database Renaming
=================

There are several ways on how to rename a database. The simplest appears to use
a script which renames all tables in conjuction with another database table 
[http://stackoverflow.com/questions/67093/how-do-i-quickly-rename-a-mysql-database-change-schema-name].


Tags
====
There are at least two major reusable django apps. one is django-tagging
and the other is django-taggit
Django tagging impairs south schema migration. It raises an NoMigration 
exception similiar as reported for django.contrib.auth 
[http://stackoverflow.com/questions/2845697/south-migration-error-nomigrations-exception-for-django-contrib-auth].
The django tagging tables are now in Denigma but the app is not installed nor 
appear the tables to be probably linked. There seems to be only a relationship 
field in link table. This tables and the link relation should probaly be 
removed via raw sql statements before it is intended to implment tagging.

django-taggit, an alternative to django-tagging also some has issues. For 
instance, tags cannot direclty be added to the admin list filter but it works 
by adding tag__name instead of tags [https://groups.google.com/forum/?fromgroups=#!topic/django-taggit/9FwdigQDrJ4]. A patch was proposed for this issue 
[https://groups.google.com/forum/?fromgroups=#!topic/django-taggit/9FwdigQDrJ4].


sqlite
======
sqlite is a leightweight sql database variant. There are two versions of 
sqlite3:

One is a python module, the other is a executable application.
The manage.py dbshell uses the latter one and complains if it is not installed 
[https://groups.google.com/forum/?fromgroups#!topic/django-users/4YMFm1C14tk[1-25]].


Domain Forwarding/Redirection
=============================

The frame redirection causes that numerous external links are not functional and sub 
folders are not displayed.

How to set up domain forwarding so that it
only replaces the base address?

Just to explain the problem:

Let's assume you have a server address (http://myserver.com) and you have
full root control over the server. You also have a domain (e.g. from 1&1) which
you can set up either to http or frame forwarding (http://mydomain.org).

If you do http-forwarding http://mydomain.com just redirects to the server
address (http://myserver.com) and subfolders
(http://myserver.com/subfolder/) are displayed correctly.

So if you made a frame forwarding to http://myserver.com and it works as it
displays http://mydomain.org in the address bar and the content of
http://myserver.com but if you when navigate on the site tree it does not show
any "subfolder", e.g. http://myserver.com/subfolder/. Rather than it
just converts everything to http://mydomain.org in the address bar.

So now the question is how to set it up that it displays the domain name
and the subfolders, e.g. http://mydomain.org/subfolder/, and only
replaces the base address of the server?
#
A possibility would be to edit the .htaccess file
[http://support.lunarpages.com/knowledge_bases/article/549].

The .htaccess file: [http://en.wikipedia.org/wiki/Htaccess].


Enabling user of .htaccess
[https://help.ubuntu.com/community/EnablingUseOfApacheHtaccessFiles].
Using .htaccess [http://www.joeldare.com/wiki/linux:using_.htaccess_on_ubuntu].
DNS setup: the full story: http://support.webvanta.com/support_article/615695-dns-setup-the-full-story#Makingthebasedomainnamework

Same issue: http://stackoverflow.com/questions/10112953/url-subfolders-not-shown-while-using-yahoo-maked-forwarding

Exactly the same problem: http://stackoverflow.com/questions/2208728/forwarding-from-domain-names-whithout-using-frames?rq=1

http://www.tonybhimani.com/2008/01/26/domain-redirection-using-apache-mod_rewrite-and-htaccess/

http://www.widexl.com/tutorials/mod_rewrite.html

Changing domain names with mod_rewrite: http://www.webmasterworld.com/forum92/152.htm
Name-based Virtual Host Support:  http://httpd.apache.org/docs/2.2/vhosts/name-based.html

redirect subdomains bar one: http://stackoverflow.com/questions/9712352/redirect-subdomains-bar-one

The solution to this dilema is to set up an A-Record in the DNS configuration 
of the domain provider. The nameserver of the provider can be used and the 
elastic IP address inserted into the configuration.


UNIX
====

Take the opportunity to venture in to the wonderful land of UNIX. It will make
your life much, much easier. If you have the option, install Linux beside your
Windows in a dual boot setting and after that, Django and ALL Django app 
godness is just one command away.

Most hosting environents use Linux, that's why it is better to use Linux for 
development too.

Linux + nginx + uwsgi = awesome


To run the server locally on a specific port, pass the ip to the manage.py by 
running it: ::

$ ./manage.py runserver 0.0.0.0:8001

or ::

$ ./manage.py runserver localhost:8002


HTML
====

Severel ways exist to change the color of a hyperlink. For instance it is 
possible toe add a style attribute and insert a color property.

<a herf="change-hyperlink-color.html", style="color: #CC0000">change hyperlink color</a>


Usage Considerations
====================

Storage of data on an EBS snapshot is cheap 
[https://forums.aws.amazon.com/message.jspa?messageID=172925].
Pricing for EBS snapshots:
- Daily: bytes*24
- Monthly:bytes*24*dayes of the months


Pinax
=====

Pinax is a framework build on top of Django that aims to provide several 
reusable apps. The latest development version is 0.9b1.dev10. The basic website 
tab is defined in templates/site_base.html and the actual text is localizable 
resource files like locale/LC_MESSAGES/django.po.
The django.po files are autogenerated via: ::

$ ./manage.py makemessages -l en

Gettext need to be installed to get this commadn work:
sudo aptitude install gettext


BitNami
=======

BitNami provides a DjangoStack for deploying projects in the cloud.
The updated BitNami stack includes  Django-1.5 (bitnami-django-stack_).
It mightbe interesting to try their images.
However it is not recommended to use any
stack as it restricts choices and overloads the server with application which 
might be not used as well as takes of the implementation details and limits 
customation.

.. _bitnami-django-stack: http://blog.bitnami.org/2012/11/django-15-beta-geodjango-support-for.html

Django
======

The high-level python-based web framework Django encourages rapid development 
and clean, pragmatic design. It was innitially developed by a fast-moving 
online-news operation. It was designed to hadle two challanges:

1. intensive deadlines of a newsroom

2. stringent requirements of expirenced Web developers.

Django allows to build high-performing, elegant Web applications quickly.


Generic forms
=============

A generic detail form as well as the admin form can not have a modifable 
created and updated field which are defined in the database model as 
auto_now_add and auto_now.


Auto-log out and failed rendering
=================================

Some views such as the Wiki and the experts invoke auto-log out and wrong 
rendering of the branding etc. It appears that adding the request context to 
the render_to_response fixes this issue. It might be because things like user site name is used in the upper most templates. Inclusion of the RequestContext is sufficient to eliminate 
this issue entirely.


Overflow
========

Longer pages lead to the inclusion of a scroll bar which provokes a shift of
the header to the left site.

It can be avoided by enforcing the scrollbar for all pages 
[http://www.daniweb.com/web-development/web-design-html-and-css/threads/336106/thirteen-ore-more-rows-in-a-table-makes-my-header-shift].

<style>body { overflow:scroll; }</style>

There are alternative solutions 
[http://hicksdesign.co.uk/journal/forcing-scrollbars-now-even-better].


Comments in CSS
===============

The synthax for commenting in CSS code is enclosing slash-asterisk:

/* comment */

/* multiline 
comment */

For details on the synthax and base data types in CSS see 
[http://www.w3.org/TR/CSS2/syndata.html].

Ctrl + F5 reloads the cached style in the browser.


EMAIL
=====

There are two major possibilities to set up an email server.
First Configure the email server yourself or use a third party provider.
There are for instance AWS SES Google Apps' gmail 
[http://stackoverflow.com/questions/5123098/aws-ses-vs-google-apps-gmail].

The Amazon Simple Email Service (SES) can be used under the Free Tier 
[http://aws.amazon.com/ses/].

Django can easily be configured to use the SES service 
[http://hmarr.com/2011/jan/26/using-amazons-simple-email-service-ses-with-django/] via django-SES.

First of all a Email address was added to the SES account and verified.

django-ses was added to the requirements/project.txt and installed locally.

Both the Email address of ADMINS and CONTACT_EMAIL was set to the Email 
address, but neither one appeared to be crucial.
AWS access and secret keys were defined in key.py as well as email backend 
(nothing else):

AWS_ACCESS_KEY_ID = 'YOUR-ACCESS-KEY-ID'

AWS_SECRET_ACCESS_KEY = 'YOUR-SECRET-ACCESS-KEY'

EMAIL_BACKEND = 'django_ses.SESBackend'

This setup was tested locally by running the server (this was not critical) and going into the

::

$ ./manage.py shell

::

>>> from django.core.mail import send_mail
>>> send_mail("Subject", "Text", 'name@xyz.com', ['name@xyz.com'], fail_silently)

Testing now whether the server need to run to get it working.

Messaging via pasted items only works by placing DEFAULT_FROM_EMAIL constant 
into the settings.

A restriction of SES is that it only allows sending Emails, but not retrieving. 
For this purpose gmail is suitable 
[http://stackoverflow.com/questions/10640507/how-to-configure-email-accounts-like-supportxyz-com-or-feedbackxyz-com-on-aws].
In such AWS SES will be used to send mail and mail will be recieved by the 
domain's Gmail user.

After creating an account by Google APPs, domains can be added by visiting
www.google.com/a/domain.tld. Following the instruction a html Email 
conformation can bea complished. Then MX records if the domain provider need
to be changed as instructed. This may take up to 24 hours.

http://www.youtube.com/watch?v=wWnf2kXOKqM

DNS stands for Domain Name System (Internet address book). CNAME are for 
subdomain [http://support.google.com/a/bin/answer.py?hl=en&answer=53340].

Evolution can be configured to access Email handled by gmail 
[https://help.ubuntu.com/community/UsingGmailWithEvolution].

Office can also be configured to directly use the domain by changing the MX 
records
[http://onlinehelp.microsoft.com/en-us/office365-enterprises/gg584186.aspx].

SES can alternatively also be used with Postman and Postix
[ Using Amazon SES in Python with Postman and Postfix], but here Django will be used.

For sending Emails via gmail account a few settings need to be declared
[http://stackoverflow.com/questions/6914687/django-sending-email].

Gmail can be used to send Emails of a specific domain via SES. However,
the Email address of this domain can not be addressed via SES as it is sayed to be blacklisted. Fortunately, it is not necessary to send Emails from Denigma to Denigma so far.  


For debugging set the following::

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

This will have the effect that it tires to send to the console instead.

Email Bounce
============
Recieved Email from SES sayng that SES account is on probationary status.

MX entries in 1&1 were gone. Reentering the values form google app gmail control panel.
Informed 1&1 service via phone and Email.

http://www.linuxquestions.org/questions/linux-server-73/gmail-rejects-email-from-my-server-why-614882/

http://www.coffeecup.com/help/articles/set-up-gmail-for-your-own-domain/

http://support.google.com/a/bin/answer.py?hl=en&answer=174125

http://support.google.com/a/bin/answer.py?hl=en&answer=37673

Django Verbose Names
====================

The representative name of a model in admin can be ovewritten via a meta class:

.. code-block:: python

    class Meta:
        verbose_name = "foo"
        verbose_name_plural = "foobars"


user access in models methods
=============================

To access current user information in the models.py for templated views the request.user should be passed to the e.g. models methods. For the Admin interface the request user can be passed in the admin.py under the method save [http://stackoverflow.com/questions/10991460/django-get-current-user-in-model-save].


Database Charset
================
The default charset in MySQL is latin1, which is suboptimal as it only provides
a very limited character set. utf8 is the apparently best coding format. To
convert a table. To convert a given table to utf8 command this: ::
    ALTER TABLE <table_name> CONVERT TO CHARACTER SET utf8;

The whole database should better have utf8 as default set and therefore a total
conversion is required.


Admin Bootstrap
===============
To install bootstrap look for the admin interface: ::

    $ git clone https://github.com/gkuhn1/django-admin-templates-twitter-bootstrap/
    $ pip install -e git+https://github.com/gkuhn1/django-admin-templates-twitter-bootstrap/#egg=django-admin-templates-twitter-bootstrap


An alternative alpha version of a restyling of the django admin done with Bootstrap
 can simple be plugged in by installing the app [https://github.com/riccardo-forina/django-admin-bootstrapped].

Other apps providing bootstrap templates for django.contrib:

- https://github.com/michaelhelmick/django-bootstrap-admin
- https://github.com/gkuhn1/django-admin-templates-twitter-bootstrap
- https://github.com/riccardo-forina/django-admin-bootstrapped
- https://github.com/aobo711/bootstrap-django-admin
- https://github.com/zbyte64/django-hyperadmin

Admin Revamp
============
A django-nuke uses a class per page and populate templates with widgets (php-nukes_).
A POC of django-hydro the widget composition framework using bootstrap
[https://github.com/amirouche/django-hydro].

django-hydro was renamed into django-composite [https://github.com/django-composite/django-composite-admin].
[https://speakerdeck.com/amiramazig/django-composite]

.. php-nuke: http://en.wikipedia.org/wiki/PHP-Nuke

UnicodeError
============

Some text raise UniCodeError when tried to print to terminal.
The follwing transformation solves this problem:
text = text.encode('ascii', 'ignore') 
[http://stackoverflow.com/questions/3224268/python-unicode-encode-error].


Favicon
=======
The small icon in the address bar is called favicon.ico [1].
There are eat least three different ways to implement it [2].
1. On apache server by adding this to the httpd.conf [2,3]: ::
    LoadModule alias_module modules/mod_alias.so
    <LocationMatch "^/favicon.ico">
        SetHandler default
    </LocationMatch>
    alias /favicon.ico /home/denigma/denigma/media/img/favicon.ico
2. On URLconf [2,4-5]: ::
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to',
       {'url': '/media/img/favicon.ico'}), # Site icon
3. In the base template header (such as theme_base.html) [2,5]: ::
    <link rel="shortcut icon" type="image/x-icon" href="/media/img/favicon.ico">
    <link href="/media/img/favicon.ico" rel="icon" type="image/x-icon">

All three were implemented but only third approach seems to work.
The respective icon was generate with GIMP by using a png to start with
If transparency is desired an alpha layer (if not allready there) and
the background color removed. The ong was scaled to 16x16 pixel (px) [6,7].

[1] http://en.wikipedia.org/wiki/Favicon
[2] http://community.webfaction.com/questions/774/create-an-icon-for-a-django-app
[3] http://www.pkshiu.com/loft/archive/2008/08/serving-favicon-in-an-django-app-using-apache
[4] http://www.netboy.pl/2011/10/add-favicon-ico-robots-txt-to-a-django-project/
[5] http://www.codekoala.com/blog/2008/setup-faviconico-django/
[6] http://www.aha-soft.com/faq/make_website_icon.htm
[7] http://tools.dynamicdrive.com/favicon/

Admin Favicon
=============
In Django-1.4 the Favicon did not appear in the admin for unknown
reason as it worked well in Django-1.3. Several ways allow to put
an favicon into the admin [http://jaredforsyth.com/blog/2010/apr/6/giving-django-admin-favicon/].


Forms
=====

Bootstrap forms
---------------
To inlcude a bootstrap form to the following [1]:

.. sourcecode:: django

   {% load bootrap_tags %}
   ...
   <form>
      <legend>A Form</legend>
      {% csrf_token %}
      {{ form|as_boostrap }}
      <div class="form-actions">
        <a href="form-actions">
        <button type="submit" class="btn btn-primary">Save changes</button>
     </div>
   </form>

Dropdown should better be triggered by hover [2-4].

[1] https://github.com/pinax/pinax-theme-bootstrap
[2] https://github.com/chrisdev/pinax-theme-foundation/pull/19
[3] http://stackoverflow.com/questions/8878033/how-to-make-twitter-bootstrap-menu-dropdown-on-hover-rather-than-click
[4] http://jsfiddle.net/ekjxu/

Crispy
------
The best way to have DRY django form is `django-crispy` form which allow to define the form in python and provides tag
and filter to quickly render forms in a div format while providing an eneromous amount of capability to configure and 
control rendered HTML [https://github.com/maraujop/django-crispy-forms]. `crispy-forms` is very well documented:
[http://django-crispy-forms.readthedocs.org/en/d-0/index.html].


Deployment
==========
The requirements are not installed on the local env.
On installing the requirements locally, it was found that MySQL-python-1.2.4b3 could not be installed
because distribute was only version 0.6.24, but version 0.6.28 is required. The same version is
installed on the global pip on deployment. It was also noted that MySQL-python had to be pythoinstalled
extra during deployment. Therefore, the most rational explaination might be that pip failed during
deployment. virtualenv & distribute shall be always kept up-to-date: ::

    . env/bin/activate
    pip install --upgrade distribute

Need ot figure out how to update virtualenv.


Getting a querysets for template forms
======================================
In order to obtain a queryset from template forms for many-to-many relationships,
the `.getlist('field') can be used on the request.POST method.


Notifications
=============
[https://github.com/yourcelf/btb/issues/3]


Customizing Styles
==================
The bootstrap hero-unit was modified to have less margin:

.. sourcecode:: css

    }
    .hero-unit {
      padding: 6px; /* 60 */
      margin-bottom: 30px; /* 3 */
      background-color: #f5f5f5; /* f5f5f5; 993399 FF99CC */ FFEEEE ffeeff
      -webkit-border-radius: 6px;
      -moz-border-radius: 6px;
      border-radius: 6px;
    }

Citations
=========
If you want to build a ship, do not drum up the men to gather the wood, divide the work and give orders.
Instead teach them to yearn for the vast and endless sea. - Antoine de Saint-Exupery

If you want to construct an Enigma do not drum up the mean to gather the pieces, divide the work and give orders.
Instead teach them to yearn the vast and endless possibilities of Denigma. - Hevok


Scalability
===========
A scalable system doesn't need to change when the size of the problem changes.
* Accommodate increased usage
* Accommodate increased data
* Maintainable.

There are two kinds of scalabality:
* Vertical scalability: buying more powerful hardware, replacing what you already own.
* Horizontal scalability: buying additional hardware, supplementing what you already own.

Horizontal scalability is the ability ro increase a system's capacity by adding more
processing units (services)


Debug Toolbar
=============
Since Django-1.4 the developmental status side bar does not react to hide any more.
Upgrading to djang-toolbar-0.9.4 solved this issue.


Scipy on Django
---------------
Scipy installation conflicts with Django which can be resolved by putting the following
into the httpd.conf which does something about sub interpreters [1]: ::

    <Directory /usr/local/www/wsgi-scripts>
        WSGIApplicationGroup %{GLOBAL}
           Order allow,deny
           Allow form all
    </Directory>

[1] http://stackoverflow.com/questions/7819588/using-scipy-stats-stats-in-django-after-deployment


Requirements Install Order
==========================
pip does not install the packages in a requirements file in order [1-2]. Install separate requirements file enables to control
the order (e.g. install numpy before Biopython).

[1] http://stackoverflow.com/questions/10937735/installing-three-packages-at-once-fails-pip-install-numpy-pil-aptus-but-indiv
[2] http://stackoverflow.com/questions/5394356/how-to-specify-install-order-for-python-pip

MySQL-python was not installed after deployment.


Hierarchy
=========
django-mptt enables the construction of relational tree structures
[http://django-mptt.github.com/django-mptt/index.html#].
To enable mptt needs added to the requirements, installed and added to the installed apps in Config::

     nano requirements/project.txt
     ...
     -e git+https://github.com/django-mptt/django-mptt/#egg=django-mptt
     ...

.. sourcecode:: python

     nano settings.py
     ...
     INSTALLED_APPS = (
     ...
     'mptt',
     ...

In order to add hierarchy to an model import `MPTTModel` and `TreeForeignKey`.
Then lets the model inherit from MPTTModel instead of models.Model and add a parent field as well as
a MPTTMeta class defining the name/title field: ::

    nano models.py
    ...
    from mptt.models import MPTTModel, TreeForeignKey
    ...
    class Classification(MPTTModel):
    ...
        parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
        ...
        class MPTTMeta:
           order_insertion_by = ['title'] # or name or something similar.
        ...
If it is added to an model with existing data it will ask for default values by doing a south data
migration. Simply specify 0 for those, but make sure to run in the ./manage.py shell tree rebuild: ::

    ./manage.py schemamigration annotations --auto
    ./manage.py migrate annotations
    ./manage.py shell
    from annotations.models import Classification
    Classification.objects.rebuild()

That is it, the model should now support hierarchical structures.
To display the hierarchy in the view/template load the `{% mptt_tags %}` template tag
and iterate over the recursetree passed data objects:

.. sourcecode:: python

    nano views.py
    ...
    def classifcations(request):
        return render_to_response("classifications.html",
                            {'nodes': Classification.objects.all()},
                            context_instance=RequestContext(request))
    ...


.. sourcecode:: django

    nano classifcations.html
    ...
    {% load mptt_tags %}
    <ul>
        {% recursetree nodes %}
            <li>
                {{ node.name }}
                {% if not node.is_leaf_node %}
                    <ul class="children">
                        {{ children }}
                    </ul>
                {% endif %}
            </li>
        {% endrecursetree %}
    </ul>
    ...

An the name of parent attribute does not to be `parent`, but than has to be specified in the MPTTMeta class:

.. sourcecode:: python

    nano models.py
    ...
    MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'category'
    ...

MPTT hierarchy can be integrated with the admin by subclasssing `MPTTModelAdmin` and registration:

.. sourcecode:: python

    nano admin.py
    ...
    from models import Classification
    ...
    from mptt.admin import MPTTModelAdmin
    ...
    class ClassificationAdmin(MPTTModelAdmin): pass
    admin.site.register(Classification, ClassificationAdmin)

However this works not well in combination with django-reversion. Either one can be used combined mixins do not
work as both provide alternative template for the list view [http://django-mptt.github.com/django-mptt/mptt.admin.html].

MPTT has `TreeManyToManyField`, thus it might be possible to have a child with more than one parent.
Althought the structure does not remain a tree anymore, it becomes a graph.

Hacker
======
A hacker is someone who strives to solve problems in elegant and ingenious
ways. Part of the path to elegantly solving problems is to use tools that solve
sub-problems very-well.


Renaming Apps
=============
The gallery app will be renamed to media to accommodate a more general purpose.
The photourl model will be renamed to image as it is more appropriate.

The many-to-many tables had to be altered manually with raw sql: ::

    ALTER TABLE data_entry_images CHANGE photourl_id image_id INT NOT NULL;
    ALTER TABLE data_change_images CHANGE photourl_id image_id INT NOT NULL;
    ALTER TABLE blog_post_images CHANGE photourl_id image_id INT NOT NULL;
    ALTER TABLE annotations_species_images CHANGE photourl_id image_id INT NOT NULL;
    ALTER TABLE annotations_tissue_images CHANGE photourl_id image_id INT NOT NULL;
    ALTER TABLE taxonomy_images CHANGE photourl_id image_id INT NOT NULL;


DAVID Annotations
=================
The DAVID API python bindings require suds. suds conflicts with the DjDt django debug toolbox.
Specifically an error is raised during authentication
[http://stackoverflow.com/questions/10071005/nonetype-object-has-no-attribute-str-in-suds].
suds-htj claims to have eliminated this issue [https://github.com/bradleyayers/suds-htj/tree/master/suds].


Running Denigma on LTS
======================
MySQLdb installation faileD with `EnvironmentError: mysql_config not found`.

    aptitude install libmysqlclient-dev
    pip install MySQL-python

Executing ./manage.py runserver fails with this error:
 _mysql_exceptions.OperationalError: (1130, "Host 'ip-10-48-111-27.eu-west-1.compute.internal' is not allowed to connect to this MySQL server")

Also the EBS appears not to be connected.
Perhaps because the secruity group need to be default.

Python Version
==============
The hypergeomtric test requires a lngamma function. Scipy provides it, but as Scipy has known
issues with virtualenv django deployment alternative solutions are seeked. Python build-in math
module provides also an lngamma function, however this was also included in 2.7+ versions.
For this reason it is considered to install Python-2.7.4 and make it to the default installation.

ln -sf /home/ubuntu/Downloads/Python-2.7.3/python /usr/bin/python

ls -l /usr/bin/python*

apt-get install python2.7

ln -s /usr/bin/python2.7 /usr/bin/python

sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 40


http://stackoverflow.com/questions/5233536/python-2-7-on-ubuntu

http://eli.thegreenplace.net/2011/10/10/installing-python-2-7-on-ubuntu/

http://www.linuxquestions.org/questions/debian-26/change-default-python-version-605397/

http://www.linuxquestions.org/questions/debian-26/how-do-i-get-apt-get-to-completely-uninstall-a-package-237772/

http://stackoverflow.com/questions/8764562/installed-a-python2-7-as-an-alternate-but-path-to-default-2-6-is-destroyed-sys

http://forums.debian.net/viewtopic.php?p=84898

http://codeghar.wordpress.com/2009/01/27/update-alternatives-in-debian/


http://devopsni.com/blog/2012/03/installing-python2-and-python3-on-ubuntu-maverick/

apt-get install python2.7
apt-get remove python-virtualenv
wget http://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.7.1.2.tar.gz
tar xzf virtualenv-1.7.1.2.tar.gz
cd virtualenv-1.7.1.2.tar.gz
/usr/bin/python2.6 setup.py install
apt-get install liblzma-de
apt-get install libgdbm-dev

wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tgz

pip install orb
orb init2.7 env

upgrading python seems to be more challenging as initial anticipated. Therefore it is considered to
deploy Denigma directly onto an Ubuntu instance with LTS 12.4 and Python-2.7 installed as default.


No module names pkg_resources
=============================
On deployment the requirement were not installed at all and checking the pip freeze in the virtualenv raised an error,
which was also raised during installation.

An apparent solution is to fix distribute with this command: ::

    curl http://python-distribute.org/distribute_setup.py | python

However, closer inspection of the root of this error gave a simplier solution. It turns out that that the distribute
installation in the virtualenv corrupts it. Therefore this command was excluded from aws-django deplyoment script: ::

    sudo pip -E /home/$LOCAL_USER/env install distribute


Virtualenvwrapper
=================
http://virtualenvwrapper.readthedocs.org/en/latest/


Database Engine
===============
Moving to the newest Ubuntu version caused issues with ForeignKeys to new created tables
[http://stackoverflow.com/questions/6178816/django-cannot-add-or-update-a-child-row-a-foreign-key-constraint-fails].
The reason for this was that the all Denigma db tables were MyISAM but the most recent version of MySQL has
InnoDB as default. Therefore all tables were converted into InnoDB in one go.

References:
http://highervisibilitywebsites.com/convert-your-mysql-database-myisam-innodb-and-get-ready-drupal-7-same-time

http://kvz.io/blog/2010/04/27/convert-all-tables-to-innodb-in-one-go/


Encoding
========

SELECT default_character_set_name FROM information_schema.SCHEMATA
WHERE schema_name = "database_name";


To switch the charset default of the entire database run: ::

    ALTER DATABASE <database_name> CHARACTER SET utf8;

mysqldump --add-drop-table database_to_correct | replace CHARSET=latin1 CHARSET=utf8 | iconv -f latin1 -t utf8 | mysql database_to_correct

mysqldump --add-drop-table denigma | replace CHARSET=latin1 CHARSET=utf8 | iconv -f latin1 -t utf8 | mysql denigma

(env)root@ip-10-227-123-178:/home/denigma# mysqldump --add-drop-table denigma | replace CHARSET=latin1 CHARSET=utf8 | iconv -f latin1 -t utf8 | mysql denigma
mysqldump: Got errno 32 on write

mysqldump --add-drop-table denigma | replace CHARSET=latin1 CHARSET=utf8 | iconv -f latin1 -t utf8 | mysql
denigma

annotation_tissue, blog_post, datasets_gendr, datasets_reference, lifespan_factor

References:
* http://codex.wordpress.org/Converting_Database_Character_Sets
* http://en.gntoo-wiki.com/wiki/Convert_latin1_to_UTF-8_in_MySQL
* http://www.bluebox.net/news/2009/07/mysql_encoding/
* http://blog.hno3.org/2010/04/22/fixing-double-encoded-utf-8-data-in-mysql/
* http://pastebin.com/iSwVPk1w
* http://en.gentoo-wiki.com/wiki/Convert_latin1_to_UTF-8_in_MySQL
* http://www.bothernomore.com/2008/12/16/character-encoding-hell/
* http://manpages.ubuntu.com/manpages/hardy/man1/iconv.1.html
* http://blog.oneiroi.co.uk/mysql/converting-mysql-latin1-to-utf8/
* http://blogs.law.harvard.edu/djcp/2010/01/convert-mysql-database-from-latin1-to-utf8-the-right-way/

Upgrading MySQL
===============
MySQL 5.6 is released an upgrade should work as described here:
[http://www.ovaistariq.net/490/a-step-by-step-guide-to-upgrading-to-mysql-5-5/]

Download binary: ::

    cd /root/
    wget http://dev.mysql.com/get/Downloads/MySQL-5.5/mysql-5.5.11-linux2.6-i686.tar.gz/from/http://mysql.llarian.net/
    http://dev.mysql.com/downloads/mysql/5.6.html


Denigma Destiny
===============
There shall always be a development version of Denigma and
eventually an experimental Destiny version which has
fundamental differences in conceptions:

| Denigma Development
| Ubuntu 12.04
| Python 2.7.3
| Django 1.4.2
| MySQL 5.5
| Engine=InnoDB
| Encoding=utf8

| Denigma Destiny
| Ubuntu 12.04
| Python 3.01
| Django 1.5.1
| PostgresSQL


Full text search
================
As InnoDB lacks full text-search, it can be supported via Sphinx http://astellar.com/2011/12/replacing-mysql-full-text-search-with-sphinx/].

Transactions
============
Bulk updates of data records can be achieved with the use of transactions.
Simply decorate the function that requires bulk update with transaction commit on success: ::

    from django.db import transaction

    @transaction.commit_on_success
    def function():
        i = 1
        entries = Entry.objects.all()
        for entry in entries:
            entry.rank = i
            i += 1

Reference:
* http://stackoverflow.com/questions/3837699/bulk-updating-a-table
* http://stackoverflow.com/questions/9521936/django-bulk-update-based-on-calculation

Apache configuration files which enabled to serve static media for the admin interface
--------------------------------------------------------------------------------------
# Steps that were undertaken to serve media but later found to be not required:

## Copy all admin media files to project media folder:
cp -a /home/denigma/env/lib/python2.6/site-packages/django/contrib/admin/media/* /home/denigma/denigma/media

## Establish a link between the admin media and served media:
sudo ln -s /home/denigma/env/lib/python2.6/site-packages/django/contrib/admin/media/ /var/www/media


Relative Path
=============
Python modules (including Django apps) have a __path__ attribute which informs where they are on
the filesystem: ::

    import os, app; path = os.path.abspath(app.__path__)

Similiar the path to the project can be set in configuration like this: ::

   PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


Shelves
=======
Inclusion of shelves for the annotation mapping algorithm leads to appearance of the following warning multiple times
whenever the development server is restarted: ::

    Exception TypeError: "'NoneType' object is not callable" in  ignored

This circumstance is well known and related ot the not properly closed shelves
[http://www.gossamer-threads.com/lists/python/dev/755445].
An solution might be to only open the shelves if an mapping will be instanced. However as long it does not appear to
cause any major performance decrease or problems it is not considered to be an main issue.

TODO list manager app.
multi-ser-functionality

Detecting Change in User Data
=============================
Changes made on the user model can be registered with the use of a "pre_save".
signale.kwargs['instance'] will contain the updated record and the old record can be
obtained with "User.obects.get(id=user.id) if user.pk else None".

Duplicated Entries
==================
Whiching entries via the Q function e.g. filtering on tags and categories, resulted in duplicated entries within the
queryset. Adding the method `distinct` on the queryset eliminated duplicates.


Markup
======
Different leightweight markup languages have all their own strength and weakenings
[http://vimeo.com/14300874].

Django markup
-------------
Django contrib markup is marked for deprication.
Therefore a replacement needs to be considered.
Some libraries are contenders in this space.

django-stify: http://code.google.com/p/django-rstify/
https://github.com/bartTC/django-markup
http://packages.python.org/django-markup/
django-MarkWhat: https://github.com/Alir3z4/django-markwhat

reStructuredText Templatetag
============================
The restructuredtext templatetag provided by django contrib markup module has 
problems with rendering the title if it appears immeditaly at the beginning.
This attributed to a normal behaviour of docutils and several there are several
solutions_. The best approach appears to be the use of the html_body instead of
fragment. Therefore an optimazed templatetag called "reST" was created.

.. _solutions: https://groups.google.com/forum/?fromgroups=#!topic/django-users/E_eOAwzCS4I


rst2pdf
=======
Converting an reST file into a PDF causes problems with the images.
It seems the error stems from being PIL having not zlib support
(rst-pil-problem_).
Prior installation of some dependencies before installing PIL with pip is claimed to resolve
this issue (install-python-imaging-library-pil_).

A possible solution path is the following (install-pil-virtualenv-on-ubuntu_):

1. Install the build dependencies: ``sudo apt-get build-dep python-imaging``
2. Symlink the libraries : ::

    sudo ln -s usr/lib/`uname -i` -linux-gnu/libfreetype.so /usr/lib/ # sudo ln -s /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/
    sudo ln -s usr/lib/`uname -i` -linux-gnu/libjpeg.so /usr/lib/ # sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
    sudo ln -s usr/lib/`uname -i` -linux-gnu/libz.so /usr/lib/ # sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/

    # Note: Substitute "i386-linux-gnu" for "x86_64-linux-gnu" if on i386

3. Install Python Image Library: ``pip install PIL``

.. _install-python-imaging-library-pil: http://askubuntu.com/questions/156484/how-do-i-install-python-imaging-library-pil
.. _rst-pil-problem: https://groups.google.com/forum/?fromgroups=#!msg/rst2pdf-discuss/4aCt9bRWSO8/ULJ9QC2-EskJ
.. _install-pil-virtualenv-on-ubuntu: http://www.sandersnewmedia.com/why/2012/04/16/installing-pil-virtualenv-ubuntu-1204-precise-pangolin/

Reportlab 2.6 does not work well with rst2pdf, although Reportlab2.5 works.
There are two possibilities either monkey path rst2pdf/reportlab or use the
older version (rst-reportlab-issue_).

The alternative is to change line 527 in rst2pdf/styles.py: ::

    reportlab.platypus.tables.CellStyle1.fontname=self['base'].fontName

    # to:

    reportlab.paltypus.tables.CellStyle.fontname=self['base'].fontName

.. _rst-reportlab-issue: http://code.google.com/p/rst2pdf/issues/detail?id=474

rst2pdf can generate presentations with the command `rst2pdf file.rst -b1 -s slides.style`
whereby file containing style information is supplied (rst-presentations_).

.. _rst-presentations: http://lateral.netmanagers.com.ar/stories/BBS52.html

SVG images are supported by rst2pdf if svglib is installed: ``pip install svglib``

To activate math install the following dependencies__: ::

    apt-get install libpng-dev libjpeg8-def libfreetype6-dev
    pip install matplotlib

.. __dependencies: http://stackoverflow.com/questions/9829175/pip-install-matplotlib-error-with-virtualenv

Further information can be found in the rst2pdf-manual_.

.. _rst2pdf-manual: http://rst2pdf.googlecode.com/svn/trunk/doc/manual.txt

rst can also alternatively be used with S5 which is a presentation way
embedded in the browser (rst2s5_)

.. _rst2s5: http://docutils.sourceforge.net/docs/user/slide-shows.html

SVG
===
svg are vectorized graphics. They can be created with for instance inkscape_.
rst2pdf can incorporate SVGs into documents, though
a library need to be installed. There are two alternative libraries producing
slightly different visual representations of SVGs (issues-with-svgs_): ::

  1. svglib: ``pip install svglib``
  2. UniConverter_

.. _inkscape: http://inkscape.org/
.. _issues-with-svgs: http://code.google.com/p/rst2pdf/issues/detail?id=188
.. _UniConverter: http://sk1project.org/modules.php?name=Products&product=uniconvertor&op=download

SVG support requires extra software installed. For best quality the `inkscape extension`_ can be used
and pdfs generated with it that can in turn be used by rst2pdf.

.. _`inkscape extension`: https://groups.google.com/forum/?fromgroups=#!topic/rst2pdf-discuss/lKbXk-c2PtM

svg2rlg_ is an updated alternative to other svg libraries.

.. _svg2rlg: https://groups.google.com/forum/?fromgroups=#!topic/rst2pdf-discuss/QXeHG_Gq8T0

Math in reST
============
There are many ways to embed math formulas into reST (math-in-reST_).

.. _math-in-reST: http://forrestyu.net/art/math-in-restructuredtext/

Thesis in reST
==============
Straight reST can be used write a `master thesis`_
and modified version of Sphinx can produce a PhD thesis (sphinxtr_).
A modified rst2html generates nice `research articles`_
A `reST API`_ is available online.
A nature science bibliothek extension of sphinx manages scientifc citations (sphinx-natbib_).

.. _`master thesis`: http://blogs.igalia.com/mrego/2009/11/23/mswl-ends-master-thesis-restructuredtext/
.. _sphinxtr: http://jterrace.github.com/sphinxtr/singlehtml/index.html#document-index.]
.. _`research articles`: http://www.loria.fr/~rougier/coding/python.html
.. _`reST API`: http://rst.projectfondue.com/
.. _sphinx-natbib: http://wnielson.bitbucket.org/projects/sphinx-natbib/
.. _latex_rest: http://comments.gmane.org/gmane.text.docutils.user/6644


Mulitplication Sign in ReST
===========================
muplication sign or related special characters can be inserted into a reST document by
`inserting the unicode character`_.


.. _`inserting the unicode character`: http://stackoverflow.com/questions/6369049/how-do-i-write-the-multiplication-sign-in-restructuredtext-rest

Autoconformation
================
In bash scripts user input questions should be autoconfirmed.
One way is to implement this automation is to flag installation commands
with -y (confirmaton-scripting_).

.. _confirmation-scripting: http://stackoverflow.com/questions/7410771/handling-input-confirmations-in-linux-shell-scripting

Unicode Characters
==================
The Unicode Transformation Format is a standard that assigns a code point (a
number) to each character in every supported language. For looking up a
character code it is here refered to a list of utf8-characters_.

.. _utf8-characters: http://www.periodni.com/unicode_utf-8_encoding.html

Denigma, the Journal of the Cutting Edge
========================================
Denigma is become a journal of the next generation. On Denigma articles are continuously peer reviewed, rather than
``one time peer-reviewed and forget about it``.


Cases-sensitivity
=================
MySQL tables with a utf8 characterset (woth utf8_unicode_ci) do not allow `case-sensitive lookups`_.
`Changing the collation status`_ to utf8_bin should resolve this issue::

    ALTER TABLE tabel_name CONVERT TO CHARACTER SET utf8 COLLATE utf8_bin;

.. 'case-sensitive lookups`: http://stackoverflow.com/questions/5354061/multiple-different-results-returned-on-case-sensitive-exact-query-in-django
.. _`Changing the collation status`: http://stackoverflow.com/questions/742205/mysql-alter-table-collation

Alternatively__::

    ALTER TABLE table_name collate=utf8_bin;

.. __: http://stackoverflow.com/questions/4784168/how-to-change-collation-to-utf8-bin-in-one-go
http://stackoverflow.com/questions/6050014/how-do-you-change-the-collation-type-for-a-mysql-column

MySQL has 4 levels of collation: server, database, table, column. Changing th collation of the server,
database or table, will not change the setting for each column, but changes the default collations.

Bad unicode data
================
A field saved as string raises the Bad unicode data Error (here title of reference fetch from Bio Entrez).
Transforming the string into unicode prior to saving the object solves this issue.

  self 	<Study: [Bad Unicode data]>
  args 	()
  e 	AttributeError("'Cursor' object has no attribute '_last_executed'",)
  kwargs 	{'title': u'TGF-\u03b2 and insulin signaling regulate reproductive aging via oocyte and germline quality maintenance.'}

Similar issues were reoprted with the utf8_bin collation (simple-non-ascii-string_).
Python decoding mechanism might also be handy with solving such  (django-unicodeerror_).

.. _simple-non-ascii-string: http://stackoverflow.com/questions/2168816/django-headache-with-simple-non-ascii-string
.. _django-unicodeerror: http://stackoverflow.com/questions/3798137/djangounicodedecodeerror-and-force-unicode


Sphinx
======
On of the greatest wonders of the world is Sphinx: the python Auto-documentation

Sphinx can be used to document python code (Using-Sphinx-to-Document-Python-Code_).
It is easy to use and will generate HTML, LaTeX, PDF, and more.

.. _Using=Sphinx-to-Document-Python-Code: http://www.youtube.com/watch?v=LQ6pFgQXQ0Q


File Permission
===============
The default apache2 group and username is www-data. It is defined in the following files:

/etc/apache2/apache2.conf
/etc/apache2/envvars

The current apache2 process user are:
[s -aux | grep apache2

chgrp -R www-data denigma/
chmod -R g+w denigma/
http://stackoverflow.com/questions/13157364/django-production-errno-13-permission-denied
http://stackoverflow.com/questions/1682440/permission-denied-error-with-django-while-uploading-a-file
http://stackoverflow.com/questions/11791833/errno-13-permission-denied-media-folder-with-localhost

Static Files
============
A static folder in the project root includes all the project-specific (and not app specific) static files.
The folder's path is then add to STATICFILES_DIRS_.
This static folder is different than STATIC_ROOT folder where the collectstatic
management command collects all `static files for deployment`_.

These need to be separated because the first once is checked into version control,
while the second is not.

.. _STATICFILES_DIRS: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-dirs
.. _`static files for deployment`: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATIC_ROOT

Insecure string pickle
======================
Fetching specific references raises ``Insecure string pickle``. It is probably caused due to
cPickles pickle behaviour. Specifically cPickle is used by shelve.

It is possible to circumvent it by using explicitly `pickle instead of cPickle`_:

.. sourcecode:: python

    import shelve
    import pickle
    shelve.Pickler = pickle.Pickler
    shelve.Unpickler = pickle.Unpickler

.. _`pickle instead of cPickle`: http://mail.python.org/pipermail/python-list/2000-February/062597.html

Sign up Customization
=====================
The account creation sign up form can apparently not been customized:

.. sourcecode:: python

    class SignupForm(GroupForm):

        username = forms.CharField(
            label = _("Username"),
            max_length = 30,
            required=False,
            widget = forms.TextInput()
        )
        password1 = forms.CharField(
            label = _("Password"),
            widget = forms.PasswordInput(render_value=False)
        )
        password2 = forms.CharField(
            label = _("Password (again)"),
            widget = forms.PasswordInput(render_value=False)
        )
        email = forms.EmailField(widget=forms.TextInput())
        confirmation_key = forms.CharField(
            max_length = 40,
            required = False,
            widget = forms.HiddenInput()
        )

        def __init__(self, *args, **kwargs):
            super(SignupForm, self).__init__(*args, **kwargs)
            if REQUIRED_EMAIL or EMAIL_VERIFICATION or EMAIL_AUTHENTICATION:
                self.fields["email"].label = ugettext("Email")
                self.fields["email"].required = True
            else:
                self.fields["email"].label = ugettext("Email (optional)")
                self.fields["email"].required = False

        def clean_username(self):

            # If no username is given try to use the nick of the email address:
            print("clean_username")
            if not self.cleaned_data["username"] and self.cleaned_data["email"] and "@" in self.cleaned_data["email"]:
                print self.cleaned_data['email']
                self.cleaned_data["username"] = self.cleaned_data['email'].split('@')[0].replace('.', '_')
                print self.cleaned_data['username'], self.cleaned_data['email']

Taggit
======
Tags are not preserved by recovering delete objects via reversion.

Twitter Bootstrap and Ajax
==========================
Ajax can be effectively used with bootstrap in a Django project (`bootstrap-ajax.js`_).
This is wonderfully illustrated in an example tasks project (`bootstrap-ajax-demo`_)

.. _`bootstrap-ajax.js`: http://paltman.com/2012/08/23/twitter-bootstrap-and-ajax/
.. _`bootstrap-ajax-demo`: https://github.com/eldarion/bootstrap-ajax-demo/blob/master/requirements.txt

Inline Input Adder
==================
The dynamic addition of form to a formset can be achieved with JavaScript (inline-input-adder_).
This was applied on the Todo app.

.. _inline-input-adder: http://stellarchariot.com/blog/2011/02/dynamically-add-form-to-formset-using-javascript-and-django/

Excluding form fields
=====================
Generally fields which should not be editable at all can be excluded from admin forms
and modelforms simply be setting ``editable=False`` as parameter in the model field definition.

In the ModelAdmin ts possible to dynamically populate the exclude attribute in get_form method.
For instance if the user is not the superuser one or more certain field(s) can be
explicitly excluded (change-a-django-form-field-to-a-hidden-field_):

.. sourcode:: python

    class EntryModelAdmin(admin.ModelAdmin):
        def get_form(self, request, obj=None, **kwargs):
            self.exclude = []
            if not request.user.is_superuser:
                self.exclude.append('field_to_hide')
            return super(EntryModelAdmin, self).get_form(request, obj, **kwargs)

For excluding form fields in non-admin forms. In the respective forms the fields can be marked as hidden.
To do this modifify/overwrite the get_context_data to include to following statement:

.. sourcecode:: python

    # views.py
    ...
    from django import forms
    ...
    class SomeView(UpdateView):
        ...
        def get_context_data(self, **kwargs):
            super(SomeView, self).get_context_data(**kwargs)
            form.fields['field_name'].widget = forms.HiddenInput()

.. sourcecode:: python

    # forms.py
    class MyModelForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
             hide_condition = kwargs.pop('hide_condition', None)
             super(MyModelForm, self).__init__(*args, **kwargs)
             if hide_condition:
                 self.fields['fieldname'].widget = forms.HiddenInput()
                 # or alternatively: del self.fields['fieldname'] to remove it from the form altogether.

.. sourcecode:: python

   # views.py
   form = MyModelForm(hide_condition=True)

A field that is set to be editable=False can still be displayed in the admin if it is marked as
being a ``readonly_fields`` (display-editable-false_):

.. sourcecode:: python

    MyModelAdmin(admin.ModelAdmin):
        readonly_fields = ('noneditable_field',)

.. _display-editable-false: http://stackoverflow.com/questions/3967644/django-admin-how-to-display-a-field-that-is-marked-as-editable-false-in-the-mo

.. _change-a-django-form-field-to-a-hidden-field: http://stackoverflow.com/questions/6862250/change-a-django-form-field-to-a-hidden-field

Non-editibale fields can even be made editible within the admin explicitly.
For this to happen a custom ModelForm needs to be declared which defines those
fields.

Dynamic ChoiceField Filtering
=============================
In order to provide a limited queryset for a select field or initial values
which depend on other instance variables one has to create dynamically on runtime
a ModelForm and passing the varibles (e.g. user) to it (runtime-choicefield-filtering-in-djangos-admin_).

.. _runtime-choicefield-filtering-in-djangos-admin: http://www.artfulcode.net/articles/runtime-choicefield-filtering-in-djangos-admin/

Incorrect Key File for Table
============================
The log entry table cannot be accessed any more on the localhost.
Trying it raises ``Incorrect key file for table.``.
It needs to be repaired (incorrect-key-file-for-table_).

.. _incorrect-key-file-for-table: http://stackoverflow.com/questions/2011050/mysql-126-incorrect-key-file-for-table

Denigma Secrets
===============
Denigma's secret projects are revolutionary ideas.

Network Visualisation
=====================
Cytoscape web, d3 [http://genemania.org/].
web-frameworks-for-network-visulation: http://grokbase.com/t/python/chicago/12638c0vtf/web-application-framework-for-network-visualization
Existing tools for generating web based network visualisation: http://www.biostars.org/p/10108/
Graph visualization code in javascript:http://stackoverflow.com/questions/7034/graph-visualization-code-in-javascript
Cytoscape web documentation: http://cytoscapeweb.cytoscape.org/documentation
Cytoscape web paper: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2935447/
HTML5 Game Development: http://www.photonstorm.com/archives/2759/the-reality-of-html5-game-development-and-making-money-from-it
20 webgl sites will blow your mind: http://www.netmagazine.com/features/20-webgl-sites-will-blow-your-mind
Learning WebGL: http://learningwebgl.com/blog/?page_id=2
ChemDoodle: http://web.chemdoodle.com/
GraphGL: https://gephi.org/tag/webgl/
#234567891123456789212345678931234567894123456789512345678961234567897123456789

Avatar
======
Checking whether an email address has a gravatar [http://mcnearney.net/blog/2010/2/15/creating-django-gravatar-template-tag-part-2/].

Encoder jpeg not available
==========================
Trying to add avatar images raises an error about missing encoder [https://github.com/dharmafly/tasket/issues/110].
IOError at /avatar/add
It can be fixed if PIL is installed from source [http://stackoverflow.com/questions/8479344/pil-encoder-jpeg-not-available].
For installing in virtual env install some prerequisites [http://www.eddiewelker.com/2010/03/31/installing-pil-virtualenv-ubuntu/].

``sudo apt=get build-dep packagename`` means
"As root, install all dependencies for `packagename` so that I can build it."
[http://superuser.com/questions/151557/what-are-build-essential-build-dep].

[http://stackoverflow.com/questions/2451352/cant-figure-out-serving-static-images-in-django-dev-environment].

MySQL returns File not found
============================
The issue can be resolved by configuring Apparmor or directly
[http://ubuntuforums.org/showthread.php?t=822084]::

    sudo nano /etc/apparmor.d/usr.sbin/mysqld
    ...
    /var/run/mysqld/mysqld.sock w,
    /data/ r,
    /data/* rw,
    ...

After reload it should be working fine::

   sudo /etc/init.d/apparmor reload


Apache Log Files
================
Apache Error Log File: /var/log/apache2/error.log
Apache Access Log File: /var/log/apache2/access.log


django-extensions
http://packages.python.org/django-extensions/

Tracking
========
django-tracking
django-tracking2
django-visitors [https://github.com/attuch/django-visitors].
django-visits counter application for bwe sites. Can count urls via CounterMiddleware and object visits (aka. models).
[https://bitbucket.org/jespino/django-visits].
chartbeat



Real-time monitoring systems:
Free trial: http://chartbeat.com/demo/
Open Source: http://piwik.org/
Google: http://www.google.com/analytics/

env Deployment
==============
* 9f2950d 2012-12-13 | Fixed the tissue hierarchy.Fixed the tissue hierarchy.etd [hevok]
git checkout 322e97c

IP Adress
=========
A GEO-ip search gives one the location of the source of an ip
 [http://rageweb.info/2011/05/15/log-messages/].
 The ip address locator for instance can perfom such a search
 [http://www.geobytes.com/iplocator.htm].
The ip-whois gives contact information of the provider
[http://www.ip-address.org/tracer/ip-whois.php].
It enables to contact the company that owns an ip address and to
report it to their abuse department. If they are serious in handling abuse issues
they'll go to the root cause of it
[http://uk.answers.yahoo.com/question/index?qid=20101103063300AA0rOah].

An api allows to display the country name [http://stackoverflow.com/questions/2218093/django-retrieve-ip-location].


GIMP
====
Creating a basic shape [http://docs.gimp.org/en/gimp-using-rectangular.html].
How to draw simple shapes in GIMP using the Pen tool
[http://emptyeasel.com/2008/08/22/how-to-draw-simple-shapes-in-gimp-using-the-pen-tool/].

Zooming 1.1000

Inkscape tutorial on creating a sphere
[http://www.youtube.com/watch?v=4OEG5zmbM_M].

Inkscape
========
Making a custom font [How to Make a Font with Inkscape].
Making a log [http://www.youtube.com/watch?v=CJt9AKkM4ZI].
How to add a new node [http://bucarotechelp.com/design/graphics/92041301.asp].
How to make own icon webfont [http://www.webdesignerdepot.com/2012/01/how-to-make-your-own-icon-webfont/].
Create texfields only via clicking not dragging as there is
bug with flowed text fields which renders them as black boxes [http://wiki.inkscape.org/wiki/index.php/FAQ#What_about_flowed_text.3F].

Sessions
========
Making sure a session is always created: http://stackoverflow.com/questions/5130639/django-setting-a-session-and-getting-session-key-in-same-view].
Get user from session key [http://scottbarnham.com/blog/2008/12/04/get-user-from-session-key-in-django/].

STATIC file of 3Party apps
==========================
The static media of the django-fluent-comment app are not found. The files were copied into the project folder.

Add Pop Up Form
===============
[http://stackoverflow.com/questions/11478647/cant-create-popup-with-tekextensions]
[https://github.com/sontek/django-tekextensions]
[http://stackoverflow.com/questions/7782479/django-reverse-engineering-the-admin-sites-add-foreign-key-button]
[http://stackoverflow.com/questions/2347582/django-admin-popup-functionality]
[http://sontek.net/blog/detail/implementing-djangos-admin-interface-pop-ups]

Ajax Form Filter
================
django-ajax-filtered-fields [http://code.google.com/p/django-ajax-filtered-fields/].
Using filter horizontal in the admin [http://stackoverflow.com/questions/3615485/django-admin-filter-horizontal].
Replicating Django's admin [http://www.hoboes.com/Mimsy/hacks/replicating-djangos-admin/].
Reuse Django's filter_horizontal admin widget [http://chase-seibert.github.com/blog/2010/05/14/reuse-djangos-filter_horizontal-admin-widget.html].
Django using admin horizontal filter in forms [http://djangosnippets.org/snippets/2466/].
Easist way to use filter horizontal outside of the admin in django [http://stackoverflow.com/questions/7778143/whats-easiest-way-to-use-filter-horizontal-outside-of-the-admin-in-django].
django-selectable [http://django-selectable.readthedocs.org/en/version-0.3.1/index.html].
django-ajax-selects [https://github.com/crucialfelix/django-ajax-selects].
Process the media class of a model form in django to a template [http://stackoverflow.com/questions/1975670/process-the-media-class-of-a-model-form-in-django-to-a-template].
django-ajax-filtered-searching the bug [http://stackoverflow.com/questions/1974671/django-ajax-filtered-fields-searching-the-bug].
ajax and django views [http://brack3t.com/ajax-and-django-views.html].


Task Management
===============
A plugeable TODO app that has been bring to completion. http://birdhouse.org/software/2008/09/django-todo/main/


http://www.youtube.com/watch?v=WcwnQW_AnC8


Voice Applcations
=================
Mumble https://github.com/mumble-voip/mumblekit
http://www.youtube.com/watch?v=Cn8bCd9n8j4

Beyond HTML5: Conversational Voice and Video demo | Ericsson Labs http://www.youtube.com/watch?v=WcwnQW_AnC8

Using the WebSocket protocol with Twisted: http://twistedmatrix.com/trac/export/29073/branches/
websocket-4173-2/doc/web/howto/websocket.xhtml

slyseal Lightweight video server [rtmp/h264/mp4] written in Python

Implementing webbased real time video chat using HTML5 websockets: http://stackoverflow.com/questions/4220672/implementing-webbased-real-time-video-chat-using-html5-websockets

Star Rating System
==================
Agon [http://agon-ratings.readthedocs.org/en/latest/usage.html]
dcramer [https://github.com/dcramer/django-ratings]
django-simple-ratings [https://github.com/dcramer/django-ratings].

A rating system can simple based on a font, and css to render e.g. "3.5 out of 5" into three and a half stars, while the html says just that.
No divs, no iimages, no Canvas, no SVG, no JavaScript, no extra spans [http://socialblogsitewebdesign.com/semantic-yet-seo-friendly-rating-stars/].

S3
==
[http://net.tutsplus.com/tutorials/tools-and-tips/use-amazon-s3-firefox-to-serve-static-files/]

Accessing both Directions of ManyToManyFields
=============================================
In order to access a ManyToManyField also in the model that does not define it,
explicitly define the field in the model form
[http://stackoverflow.com/questions/4316606/how-to-access-both-directions-of-manytomanyfield-in-django-admin]:

For instance, assume data entries shall be have many to many relations with dataset references.

First define that dataset uses data entries as categories via a many to many relation:

.. sourcecode:: python

    # dataset.models:
    form django.db import models


    class Reference(models.Model):
        pmid = models.IntegerField()
        categories = models.ManyToManyField('data.Entry')


In the data form define the references field explicitly:

.. sourcecode:: python

    # data.forms:
    from django import forms

    from datasets.models import Reference

    from models import Entry


    class EntryForm(forms.ModelForm):
        references = forms.ModelMultipleChoiceField(
            label="References",
            queryset=References.objects.all(),
            required=False,
            help_text="References to the literature",
            widget=admin.widgets.FilterSelectMultiple('references, False)
        )
        class Meta:
            models = Entry

The form can be employed outside as well as inside the admin:

.. sourcecode:: python

    # data.admin:
    from django.contrib import admin

    class EntryAdmin(admin.ModelAdmin):
        fields = ('references',)

        def safe_model(self, request, obj, form, change):
            # Save without m2m field (can not save them unti obj has id):
            super(EntryAdmin, self).save_model(request, obj, form, change):
            # If it worked, deal with m2m fields:
            obj.references.clear()
            for reference in form.cleaned_data['references']:
                obj.references.add(reference)

        def get_form(self, request, obj=None, **kwargs):
            if obj:
                self.form.base_fields['references'].initial = [o.pk for o in obj.references.all()]
            else:
                self.form.base_fields['references'].initial = []
            return super(EntryAdmin, self).get_form(request, obj, **kwargs)


    admin.site.register(Entry, EntryAdmin)


Front-End
=========
Front end frameworks allow to build pages faster
[http://foundation.zurb.com/; http://twitter.github.com/bootstrap/].
It is even more accelerated by the use of theme/base generators
[http://jetstrap.com/; http://www.boottheme.com/].
They give the html and bootstrap.css or variables.less to integrate into a project.


Front end analysis can provide great infos on traffic:
[http://dj-wat.blogspot.de/2010/06/announcement-chat-queries.html]

Multiple Sites
==============
The "site" framework [https://docs.djangoproject.com/en/dev/ref/contrib/sites/?from=olddocs].
Django: cofiguring multiple domains for a website [http://stackoverflow.com/questions/7580306/django-configuring-multiple-domains-for-a-website]
Using Subdomains in Django [http://thingsilearned.com/2009/01/05/using-subdomains-in-django/].
[http://stackoverflow.com/questions/1553165/multiple-django-sites-with-apache-mod-wsgi].

AWS
===
Best database solution for Django on AWS [http://stackoverflow.com/questions/9842961/best-database-solution-for-django-on-aws].



Wrong Permission
================
To enable ftp access to other developer the key-pair need to be shared.
Trying to generate a new key-pair and using it to access an instance raises the following issue:

The authenticity of host 'ec2-46-137-15-178.eu-west-1.compute.amazonaws.com (46.137.15.178)' can't be established.
ECDSA key fingerprint is 72:e7:40:75:d3:ad:c3:55:1c:4c:34:77:3a:4c:6a:05.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'ec2-46-137-15-178.eu-west-1.compute.amazonaws.com,46.137.15.178' (ECDSA) to the list of known hosts.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0664 for 'kp.pem' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
bad permissions: ignore key: kp.pem
Permission denied (publickey).

Appearentely it is duo to having the wrong mod on the file which was solved by
[http://stackoverflow.com/questions/8193768/trying-to-ssh-into-an-amazon-ec2-instance-permission-error]:

    chmod 400 dp.pem

#234567891123456789212345678931234567894123456789512345678961234567897123456789

Circular import
===============
The caching of the rendered data entries
http://stackoverflow.com/questions/6923042/avoid-circular-model-imports-in-django-apps

update-apt-xapi
===============
The update-apt-xapi started without any reason and took all the resources: http://ubuntuforums.org/showthread.php?t=1086435