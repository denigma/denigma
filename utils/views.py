from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib import messages

class ExtraContextView(TemplateView):
    """Compensates for the missing extra_context argument which was
    available in old-style generic views.

    Usage:

        urlpatterns = patterns('',
            (r'^aurl/$", ExtraContextView.as_view(
                template_name='template.html',
                extra_context={
                    ...}
    """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContextView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def reverse_and_redirect(view, *args, **kwargs):
    """Returns a RedirectView which will reidrect ot a url determined by reversing the
    given parameters. The reverse is lazy in that it won't be evaluted until needed."""
    class _Redirect(RedirectView):
        def get_redirect_url(self, **k):
            return reverse(view, args=args, kwargs=kwargs)

    return _Redirect.as_view()


class MessageMixin(object):
    """Make it easy to dispaly notification messages when using Class Based Views."""
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MessageMixin, self).delete(request, *args, **kwargs)

    def form_valid(self, request, form):
        messages.success(self, request, self.success_message)
        return super(MessageMixin, self).form_valid(form)


class RequestCreateView(MessageMixin, CreateView):
    """Sub-class of CreateView to automatically pass the Request to the Form."""
    success_message = "Created Successfully"

    def get_form_kwargs(self):
        """Add the Request object to the form's keyword arguments."""
        kwargs = super(RequestCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class RequestUpdateView(MessageMixin, UpdateView):
    """Sub-class the UdpateView to pass teh request ot the form and limit the
    queryset to the requesting user."""
    success_message = "Updated Successfully"

    def get_form_kwargs(self):
        """Add the Request object to te form's keywords arguments."""
        kwargs = super(RequestUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_queryset(self):
        """Limit a user to only modfying their own data."""
        qs = super(RequestUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class RequestDeleteView(MessageMixin, DeleteView):
    """Sub-class the DeleteView to restrict a User from deleting other
    user's data.

    Usage:

        from utils.views import RequestDeleteView

        url(r'^delete-photo/(?P<pk>[\w]+)/$', RequestDeleteView.as_view(
                    model=Photo,
                    success_url='/site/media/photos',
                    template_name='site/media-photos-delete.html',
                    success_message='Your Photo has been deleted successfully.',
                    ), name='delete-photo-form'),
#234567891123456789212345678931234567894123456789512345678961234567897123456789

    """
    success_message = "Deleted Successfully"

    def get_queryset(self):
        qs = super(RequestDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)