=================
Upgrading Denigma
=================

Denigma Django version will be upgraded from 1.3 to 1.4.


Importing Settings
------------------
Move the manage.py into the outer project folder and the following lines: ::
    import sys
    import os
    ...
    try:
        import denigma.settings as settings_mod # Assumed to be in the same directory.
    ...
    if __name__ == "__main__":
         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "denigma.settings")
         ...

Template Loader
---------------
Starting the development server and commenting out all the applications urls raised the following Exception Value:

Error importing template source loader django.template.loaders.filesystem.load_template_source:
"'module' object has no attribute 'load_template_source'"

To resolve this the depricated load_template_source was commented out and the respective Loaders included: ::

     nano settings.py
     ...
     TEMPLATE_LOADERS = [
         'django.template.loaders.filesystem.Loader',
         'django.template.loaders.app_directories.Loader'
         #'django.template.loaders.filesystem.load_template_source',
         #'django.template.loaders.app_directories.load_template_source',
         ...


URLs
----

Next the profiles and notices urls in URLconf were activated.
However activating notifications raised exception as feed can not be imported
Renaming feed to Feed or upgrading django-notification seems to solve this issues.
[https://github.com/yourcelf/btb/issues/3]: ::

     pip install --upgrade django-notifications # well this appears to be the wrong notifications.

This did not resolve the issue, anyway.

However, replacing the django-notification source link in the requirements/base.txt,
deinstalling django-notification and reinstalling the new branch seems to fix this problem.


Now another issue regarding accounts: ::

Exception Type: 	NoReverseMatch
Exception Value: Reverse for 'acct_email' with arguments '()' and keyword arguments '{}' not found.

Exception Value: u'admin' is not a registered namespace

Activating the accounts url solves this.

Activate admin, news.

Congratulation Denigma is now running 1.4!

All urls were activated.

The aspects/urls.py had to be modified.
Specifically the add_achievement and title had to be given proper names ::

    ...
    url(r'^achievement/add', 'add_achievement', name='add_achievement'),
    ...
    url(r'^design/title/(?P<name>\w+)', 'title', name='title'),
    ...


Still the notification is down because of several conceptional changes to its structure.

Exception Value: Reverse for 'notification_feed_for_user' with arguments '()' and keyword arguments '{}' not found.

Error during template rendering
Exception Value: Reverse for 'notification_feed_for_user' with arguments '()' and keyword arguments '{}' not found.
In template /home/daniel/testing/denigma14/denigma/env/local/lib/python2.7/site-packages/pinax_theme_bootstrap/templates/notification/base.html, error at line 6

To resolve this the respective template was copied into the project dir and extra_head block was commented out: ::

    cp /home/daniel/testing/denigma14/denigma/env/local/lib/python2.7/site-packages/pinax_theme_bootstrap/templates/notification/base.html /home/daniel/testing/denigma14/denigma/denigma/templates/notification/base.html
    nano base.html
    ...
    {% comment %} Feed is removed from the current notification branch {% block extra_head %}
        <link rel="alternate" type="application/atom+xml" title="Notices Feed" href="{% url notification_feed_for_user %}" />
    {% endblock %}{% endcomment %}
    ....

Sending an message now raises the following warning: ::
Exception Type: 	Warning
Exception Value: 	Data truncated for column 'medium' at row 1

Migrating the NoticeSetting model is required as its medium field max_length was
extended from 1 to 16.

Sending message again raises another exception: ::
Exception Type: 	IntegrityError
Exception Value:

(1062, "Duplicate entry '2-3-e' for key 'user_id'")

From this it appears easier to simply copy notification into the project and rename feed
to Feed.

    cp -rf /home/user/denigma/env/lib/python2.7/site-packages/notification /home/user/denigma/denigma/apps/notification
    nano notification/views.py
    ...
    from django.contrib.syndication.views import Feed # feed
    ...
    return Feed(request, url, { # exhanged feed by Feed. Does it actually work?
    ...

Reversion
---------
Need to install another version of reversion as changing a data/entry blog/post raises the
following exception: ::
Exception Value: 	'PostAdmin' object has no attribute 'inline_instances'
Exception Location: 	/home/daniel/testing/denigma14/denigma/env/local/lib/python2.7/site-packages/reversion/admin.py in render_revision_form, line 299

This does not occur in Django-1.5 with the appropiate version of reversion.

According to the reversion docs while Django-1.3.2 is compatible with Reversion-1.5.3,
Django-1.4.1 is compatible with the current latest version of reversion, i.e.
Reversion-1.6.2.

    pip install --upgrade django-reversion. # This installed django-Reversion-1.6.3.

Testing.

Got error:

Exception Type: 	AttributeError
Exception Value: 'functools.partial' object has no attribute '__name__'

Broke code.

Uninstalling reversion-1.6.3 and reinstalling reversion-1.5.3 restored integrity.

Debug toolbar has probably to be updated.
Current version is: django-debug-toolbar==0.9.1

   pip install --upgrade django-debug-toolbar

Solved!

Worked like a charm.


AWS-Deployment modification
---------------------------

Included installing updating distribute  both global and local:

install_apache() {
    apt-get install -y apache2 libapache2-mod-wsgi
    pip install virtualenv
    pip install upgrade distribute
}

install_project() {
    if [ -f $DISTRIBUTION ]; then
        LOCAL_DISTRIBUTION_PATH=$DISTRIBUTION
    fi
    sudo pip -E /home/$LOCAL_USER/env install distribute
    sudo pip -E /home/$LOCAL_USER/env install -r $PROJECT_ROOT/requirements/project.txt
}

Removed the following line from install_project as it is already shiped with:

     sudo cp -rf /home/$LOCAL_USER/env/lib/python2.6/site-packages/pinax_theme_bootstrap/static/. /$PROJECT_ROOT/media

Correcting Path to manage.py: ::

django_syncdb() {
    sudo /home/$LOCAL_USER/env/bin/python /home/$LOCAL_USER/manage.py syncdb --noinput
}

After deploying Denigma, def had to be renamed to denigma, which is suboptimal.
pip freeze gave this results:

BeautifulSoup==3.2.1
distribute==0.6.28
wsgiref==0.1.2

Manually started the installation of the requirements: ::

    pip install -r requirements/project.txt

Need to change the local_settings.py and set django.db.backends.mysql: ::

    nano local_settings.py
    ...
    DATABASES = {
        "default": {
           "ENGINE": "django.db.backends.mysql",
           ...

DONE!

Final issue, pinax/bootstrap statics is not loaded correctly. Need to copy statics into project app.
This command should be done by the django-aws.

Unfortunely, the admin has no style. http://stackoverflow.com/questions/1833675/django-admin-has-no-style
For django-1.4 apache `Alias /static/admin /home/denigma/env/lib/site-packages/django/contrib/admin/static/admin

    nano /home/denigma/denigma/settings.py
    ...
    # URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
    # trailing slash.
    # Examples: "http://foo.com/media/", "/media/".
    ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, 'admin/')

    nano /etc/apache2/site-available/denigma # Note also in django-aws
    ...
    Alias /admin/media /home/$LOCAL_USER/env/lib/python2.6/site-packages/django/contrib/admin/media/
     <Directory "/home/$LOCAL_USER/env/lib/python2.6/site-packages/django/contrib/admin/media">
    ...

    nano /home/denigma/django-aws
    sudo echo "Alias /django/contrib/admin/media/ /home/$LOCAL_USER/env/lib/python2.6/site-packages/django/contrib/admin/media/" >> /etc/apache2/httpd.conf


    nano /home/denigma/denigma/local_settings.py
    ...
    ADMIN_MEDIA_PREFIX = '/django/contrib/admin/media/'
    ...

Renaming to: ::

   Alias /admin/static /home/$LOCAL_USER/env/lib/python2.6/site-packages/django/contrib/admin/static/admin/
    <Directory "/home/$LOCAL_USER/env/lib/python2.6/site-packages/django/contrib/admin/static/admin">


Check out apache2 logs
----------------------
[http://www.cyberciti.biz/faq/apache-logs/]
/var/log/apache2/error.log # Nothing obvious.
/var/log/apache2/access.log # Empty


Lastly, copy the key file and check Email support.
