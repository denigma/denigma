from django import forms
from django.utils.safestring import mark_safe
from pagedown.widgets import PagedownWidget


class SectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        """Add a field for every question.
        Field may be CharField or ChoiceField; field name is question.order."""
        section = kwargs.pop("section")
        self.name = section.name
        self.description = section.description
        self.total = section.questionnaire.sections.count()
        super(SectionForm, self).__init__(*args, **kwargs)

        self.footnotes = ''
        for question in section.questions.all():
            choices = question.choices
            if question.footnote:
                #question.question.split('')[1].split('*')
                self.footnotes += question.footnote+'<br>'

            kw = dict(help_text=question.question, required=False)
                       #'style': 'font-family: monospace',
                       #'class':'wmd-input', 'id': 'wmd-input'

            if choices:
                fld = forms.ChoiceField
                choices = [c.strip() for c in choices.split(',')]
                kw["choices"] = [(c,c) for c in choices]
            else:
                fld = forms.CharField
                #kw["max_length"] = 200
                kw['widget'] = PagedownWidget(attrs={'rows': 1, 'cols': 1})

            if not "Stages" in self.name:
                self.fields[str(question.order)] = fld(**kw)
            else:
                self.fields[str(question.order)+'-help'] = fld(**kw)
                self.fields[str(question.order)+'-risk'] = fld(**kw)
