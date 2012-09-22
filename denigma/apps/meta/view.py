"""Log changes outside the admin"""
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode


def log(request, object, comment=None):
    """Takes a request and a model object and generats a log entry."""
    LogEntry.objects.log_action(
        user_id = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id = object.pk,
        object_repr = force_unicode(object),
        action_flag = ADDITION,
        change_message = comment
    )

    #    # Log Entry:
    #    log_entry = LogEntry(
    #        object_id = post.id,
    #        action_flag=ADDITION,
    #        content_type__id__exact=ContentType.objects.get_for_model(Post).id,
    #        user=request.user,
    #        change_message=comment)
    #    log_entry.save()