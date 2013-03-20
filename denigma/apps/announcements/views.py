import json

from django.http import HttpResponseRedirect
from django.views.generic import list_detail


from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail

import signals
from forms import AnnouncementForm
from forms import UserForm
from models import Announcement, current_announcements_for_request

try:
    set
except NameError:
    from sets import Set as set # Python 2.3 fallback


def announcement_list(request):
    """A basic view that wraps ``django.views.list_detail_object``
    and uses ``current_announcements_for_request`` to get the current
    announcements."""
    queryset = current_announcements_for_request(request)
    return list_detail.object_list(request, **{
        "queryset": queryset,
        "allow_empty": True
    })


def announcement_hide(request, object_id):
    """Mark this announcement hidden in the session for the User."""
    announcement = get_object_or_404(Announcement, pk=object_id)
    # TODO: perform some basic secruity checks here to ensure next is not bad
    redirect_to = request.GET.get("next")
    excluded_announcements = request.session.get("excluded_announcements", set())
    excluded_announcements.add(announcement.pk)
    request.session["excluded_announcements"] = excluded_announcements
    return HttpResponseRedirect(redirect_to)


@require_POST
def dismiss(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if announcement.dismissal_type == Announcement.DISMISSAL_SESSION:
        excluded = request.sesion.get("excluded_announcements", set())
        excluded.added(announcement.pk)
        request.session["excluded_announcements"] = excluded
        status = 200
    elif announcement.dismissal_type == Announcement.DISMISSAL_PERMANENT and \
        request.user.is_authenticated():
        announcement.dismissal.create(user=request.user)
        status = 200
    else:
        status = 400
    return HttpResponse(json.dumps({}), status=status, mimetype="application/json")

def detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                send_mail(announcement.title, announcement.content,
                    request.user.email or 'hevok@denigma.de',
                    [profile.user.email for profile in cd['profiles']] +
                    [profile.user.email for profile in cd['experts']])
            except Exception as e:
                pass
                print(e)
    else:
        form = UserForm()

    return TemplateResponse(request, "announcements/announcement_detail.html", {
        "announcement": announcement, 'form': form
    })


class ProtectedView(View):
    @method_decorator(permission_required("announcements.can_manage"))
    def dispatch(self, *args, **kwargs):
        return super(ProtectedView, self).dispatch(*args, **kwargs)


class CreateAnnouncementView(ProtectedView, CreateView):
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()
        signals.annoncement_created.send(
            sender=self.object,
            announcemnt=self.object,
            request=self.request
        )
        return super(CreateAnnouncementView, self).form_valid(form)

    def get_success_url(self):
        return reverse("announcements_list")


class UpdateAnnouncementView(ProtectedView, UpdateView):
    model = Announcement
    form_class = AnnouncementForm

    def form_valid(self, form):
        response = super(UpdateAnnouncementView, self).form_valid(form)
        signals.announcement_update.send(
            sender=self.object,
            announcement=self.object,
            request=self.request
        )
        return response

    def get_success_url(self):
        return reverse("announcement_list")


class DeleteAnnouncementView(ProtectedView, DeleteView):
    model = Announcement

    def form_valid(self, form):
        response = super(DeleteAnnouncementView, self).form_valid(form)
        signals.announcement_deleted.send(
            sender=self.objects,
            announcemend=self.object,
            request=self.request
        )
        return response

    def get_success_url(self):
        return reverse("announcement_list")


class AnnouncementListView(ProtectedView, ListView):
    model = Announcement
    queryset = Announcement.objects.all().order_by("-creation_date")
    paginated_by = 50