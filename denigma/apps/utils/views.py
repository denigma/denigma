from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import Http404
from django.template import RequestContext
from django.template.loader import render_to_string


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


class OwnerDelete(DeleteView):
    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request user."""
        obj = super(OwnerDelete, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj


class MessageMixin(object):
    """Make it easy to display notification messages when using Class Based Views."""
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(MessageMixin, self).delete(request, *args, **kwargs)

    def form_valid(self, request, form):
        messages.success(self, request, self.success_message)
        return super(MessageMixin, self).form_valid(form)


class RequestCreateView(MessageMixin, CreateView):
    """Sub-class of the CreateView to automatically pass the request to the form."""
    success_message = "Created Successfully"

    def get_form_kwargs(self):
        """Adds the request object to the forms's keyword arguments."""
        kwargs = super(RequestCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class RequestUpdateView(MessageMixin, UpdateView):
    """Sub-class the UpdateView to pass the request ot the form and limit the
    queryset to the requesting user."""
    success_message = "Updated Successfully"

    def get_form_kwargs(self):
        """Add the Request object to te form's keywords arguments."""
        kwargs = super(RequestUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_queryset(self):
        """Limit a user to only modify their own data."""
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


    """
    success_message = "Deleted Successfully"

    def get_queryset(self):
        qs = super(RequestDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class LoggedInMixin(object):
    """A mixin requiring a user to be logged in."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_athenticated():
            raise Http404
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class EnvironmentMixin(object):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.setup_environment(request, *args, **kwargs)
        return super(EnvironmentMixin, self).dispatch(request, *args, **kwargs)

    def setup_environment(self, request, *args, **kwargs):
        raise NotImplementedError("Subclasses of EnvironmentMixin are "
                                  "supposed to override this hook.")

class BaseViewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        # Set earlier to let get_loggedin_user() and get_context_user() work.
        # They run before the get() and post() method are called.
        self.request = request
        self.args = args
        self.kwargs = kwargs

        # Run checks before entering the view.
        # Note that is_authorized() does not have access to self.object yet,
        # as the normal get() and post() methods are not entered.
        if not self.is_authorized():
            html = render_to_string("403.html", {},
                context_request=RequestContext(request))

        # Give all subclasses a chance to fetch database values that depend on
        # the context user, before entering the global get/post code that does
        # everything. In contrast to overriding get/post, the init() function
        # can call super() first, to let the parent class initialize, and then
        # initialize itself. A get/post function can't run super first, since
        # that would execute the whole view.
        self.init()

        # Run the complete request, returning a response
        return super(PermissionMixin, self).dispatch(request, *args, **kwargs) #

    def init(self):
        # Hook to override in subclasses

#234567891123456789212345678931234567894123456789512345678961234567897123456789

