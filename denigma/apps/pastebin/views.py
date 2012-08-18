"""View function that is in charge of the form for submitting new items."""
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, get_host
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from models import PastedItem
from forms import PastedItemForm


def new(request, form_class=PastedItemForm, template_name="pastebin/new.html"):
    """Form for pasting new items."""
    form = form_class()
    if request.method == 'POST':
        if request.POST["action"] == "paste":
            form = form_class(request.user, request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.user = request.user
                item.save()
                request.user.message_set.create(
                    message=ugettext("The new pasted item was saved."))
                    # Some problem with ugettext_lazy here.
                return HttpResponseRedirect(reverse('pastebin_detail',
                                            args=(item.uuid,)))
    return render_to_response(template_name,
                            { "form": form, },
                            context_instance=RequestContext(request))

new = login_required(new)
