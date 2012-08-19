from django.db.models import signals, get_app
from django.utils.translation import ugettext_noop as _
from django.core.exceptions import ImproperlyConfigured


try:
    notification = get_app('notification')

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type(
            "pasteditem_received",
            _("Pasted Item Received"),
            _("you have received a pasted item"))
        notification.create_notice_type(
            "pasteditem_sent",
            _("Pasted Item Sent"),
            _("you sent a pasted item"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImproperlyConfigured:
    print("Skipping creation of NoticeTypes as notification app not found.")
