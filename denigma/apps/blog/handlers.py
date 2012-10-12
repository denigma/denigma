from django.contrib.auth.models import User
from django.core.mail import send_mail


def notify_admin(sender, instance, created, **kwargs):
    '''Notify the administrator that a new user has been added.'''
    if created:
        subject = 'New post created'
        message = 'Post %s was added.' % instance.title
        from_addr = 'hevok@denigma.de'
        recipient_list = ('age@liv.ac.uk',)
        send_mail(subject, message, from_addr, recipient_list)