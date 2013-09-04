"""View function that is in charge of the form for submitting new items."""
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from models import PastedItem
from forms import PastedItemForm, SendItemForm


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

##                request.user.message_set.create(
##                    message=ugettext("The new pasted item was saved."))
                    # Some problem with ugettext_lazy here.
                    # Create does not work, but add message to messages works: 
                messages.add_message(request, messages.SUCCESS,
                    ugettext("The new pasted item was saved."))
                    
                return HttpResponseRedirect(reverse('pastebin_detail',
                                            args=(item.uuid,)))
    return render_to_response(template_name,
                            { "form": form, },
                            context_instance=RequestContext(request))
new = login_required(new)


def detail(request, uuid, form_class=SendItemForm,
           template_name='pastebin/pasteditem_detail.html'):
    """View that shoes a pasted item and will also act on this form's data."""
    form = form_class()
    if request.method == 'POST':
        if request.POST["action"] == "send":
            form = form_class(sender=request.user, data=request.POST)
            if form.is_valid():
                form.save()

##                request.user.message_set.create( 
##                    message=ugettext("The pasted item was sent."))
                # Create does not work, but add message to messages works:              
                messages.add_message(request, messages.SUCCESS,
                    ugettext("The pasted item was sent to %(user)s.") % {
                        "user": SendItemForm.clean_recipient(form)})
                
                
                url = form.pasted_item.get_absolute_url()
                return HttpResponseRedirect(url)
    pasted_item = get_object_or_404(PastedItem, uuid=uuid)
    return render_to_response(template_name,
                               { 'object': pasted_item, 'form': form },
                               context_instance=RequestContext(request))
#detail = login_required(detail)
