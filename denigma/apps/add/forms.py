from django.template.loader import render_to_string
from django import forms
from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render

import reversion

from meta.view import log


class SelectWithPop(forms.Select):
    def render(self, name, *args, **kwargs):
        html = super(SelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name})

        return html+popupplus


class MultipleSelectWithPop(forms.SelectMultiple):
    def render(self, name, *args, **kwargs):
        html = super(MultipleSelectWithPop, self).render(name, *args, **kwargs)
        popupplus = render_to_string("form/popupplus.html", {'field': name, 'multiple': True})

        return html+popupplus


def handlePopAdd(request, addForm, field, template="form/popadd.html"):
    if request.method == "POST":
        form = addForm(request.POST)
        if form.is_valid():
            try:
                with reversion.create_revision():
                    newObject = form.save()
                    reversion.set_user(request.user)
                    comment = request.POST['comment'] or 'Added.'
                    reversion.set_comment(comment)
                    log(request, newObject, comment)
            except forms.ValidationError, error:
                newObject = None
            if newObject:
                return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                                    (escape(newObject._get_pk_val()), escape(newObject)))
    else:
        form = addForm()

    ctx = {'form': form,'field': field}
    return render(request, template, ctx)