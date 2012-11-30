from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext # For csrf
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required

from models import Item
from forms import ListForm, ItemForm


def index(request):
    """Function used to make empty formset forms required."""
    class RequiredFormSet(BaseFormSet):
        def __init__(self, *args, **kwargs):
            super(RequiredFormSet, self).__init__(*args, **kwargs)
            for form in self.forms:
                form.empty_permitted = False
    ItemFormSet = formset_factory(ItemForm, max_num=10, formset=RequiredFormSet)
    if request.method == 'POST': # If the form has been submitted...
        list_form = ListForm(request.POST) # A form bound to the POST data.
        # Create a formset form the submitted data.
        item_formset = ItemFormSet(request.POST, request.FILES)

        if list_form.is_valid() and item_formset.is_valid():
            list = list_form.save()
            for form in item_formset.forms:
                item = form.save(commit=False)
                item.list = list
                item.save()
            return HttpResponseRedirect('thanks') # Redirect to a 'success' page.

    else:
        list_form = ListForm()
        item_formset = ItemFormSet()

    # For CSRF protection:
    c = {'list_form': list_form,
         'item_formset': item_formset
        }
    c.update(csrf(request))

    return render_to_response('todo/index.html', c)

@staff_member_required
def mark_done(request, pk):
    """Marks a todo as done."""
    item = Item.objects.get(pk=pk)
    item.done = not item.done
    item.save()
    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def delete(request, pk):
    """Deletes a todo quickly via the queryset deletion."""
    Item.objects.filter(pk=pk).delete()
    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def onhold(request, pk):
    """Holds on a todo."""
    item = Item.objects.get(pk=pk)
    item.onhold = not item.onhold
    item.save()
    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def item_action(request, action, pk):
    """Mark done, toggle onhold or delete a todo item."""
    if action == "done":
        item = Item.objects.get(pk=pk)
        item.done = not item.done
        item.save()
    elif action == "onhold":
        item = Item.objects.get(pk=pk)
        item.onhold = not item.onhold
        item.save()
    elif action == "delete":
        Item.objects.filter(pk=pk).delete()

    return HttpResponseRedirect(reverse("admin:todo_item_changelist"))

@staff_member_required
def onhold_done(request, mode, action, pk):
    """Toggle Done / Onhold on/off."""
    item = Item.objects.get(pk=pk)

    if action == "on":
        if mode == "done": item.done = True
        elif mode == "onhold": item.onhold = True
    elif action == "off":
        if mode == "done": item.done = False
        elif mode == "onhold": item.done = False
    item.save()
    return HttpResponse('')

def progress(request, pk):
    """Set todo progress."""
    p = request.POST
    if "progress" in p:
        item = Item.objects.get(pk=pk)
        item.progress = int(p["progress"])
        item.save()
    return HttpResponse('')
