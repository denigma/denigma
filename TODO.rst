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
users can access all the data structure behind Denigma and change to the 
shape and content of its underlying database which will be tracked back to 
the user and and time of change. In such we don't run in the risk that 
someone corrupts the database. We can just go back and reverse any wrong 
changes.

While south tracks all changes in database schema, The backup app (code name 
north) save/tracks all changes to the content of an app. If a entry gets 
deleted it will be backuped. If the title or centent of an entry is changed the 
changes will be saved with associated meta data such as modifing user and time 
of modification. The changes must be able to be visualised so that it is 
possible revisit the history of an entry. 

Signing up is made simple. All what is required for now is just a user name and 
a password for identifying an individual.


Simplifing Account Creation
---------------------------

User account creation can be even more simplified for known experts. The 
default user name will be assumed to be FirstName_LastName. Only the Email 
field is required and password will be send by email. User names actually need 
to be changeable too.


Global Site-wide Search
-----------------------

Denigma needs a umnipotent search function which is able to search all fields 
of all tables or only a specified subset as it was similiar implemented in 
Denigma's Wiki.

There are numerous ways on how to implement searching. One option would be 
Haystack/Whoosch and another Xapian/Djapian
[http://www.vlent.nl/weblog/2010/10/14/searching-django-site-part-1-what-and-why/].


The Future of Denigma
---------------------

This is just the beginning. Further DEPs might be:

- Need to get GIT from Denigma server working.
- restore.sh for restoring a snapshotted database.
- Automate EC2 instance setup
  [http://www.turnkeylinux.org/blog/ec2-userdata].
- Use Fabric for ssh control of Denigma 
  [http://docs.fabfile.org/en/1.4.3/index.html].
- Move Denigma db to RDS.

May Denigma's future be bright!

#234567891123456789212345678931234567894123456789512345678961234567897123456789

