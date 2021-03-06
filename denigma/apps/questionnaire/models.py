from string import join

from django.db.models import CharField, TextField, ForeignKey, IntegerField, DateTimeField, BooleanField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from utils import BaseModel, reverse2


link = "<a href='%s'>%s</a>"


class  Questionnaire(BaseModel):
    name = CharField(max_length=255, unique=True)
    description = TextField()
    published = BooleanField(default=True)
    section_footnotes = {}

    def __unicode__(self):
        return self.name

    def get_absolute_url(self, section=1):
        return reverse2("questionnaire", self.pk, section)

    def section_links(self):
        section_url = "admin:questionnaire_section_change"
        lst = [(c.pk, c.name) for c in self.sections.all()]
        lst = [(reverse2(section_url, pk), name) for pk, name in lst]
        return ", ".join([link % c for c in lst])
    section_links.allow_tags = True

    def get_section(self, str):
        for section in self.sections.all():
            if str == section.name:
                return section



    def get_length(self):
        return len(self.sections)


class Section(BaseModel):
    """Container for a few questions, show on a single page."""
    name = CharField(max_length=60, blank=True, null=True)
    description = TextField(blank=True)
    questionnaire = ForeignKey(Questionnaire, related_name="sections", blank=True, null=True)
    order = IntegerField()
    start = IntegerField(default=1)

    class Meta:
        ordering = ["order"]
        unique_together = [["questionnaire", "order"]]

    def __unique__(self):
        return "[%s] (%s) %s" % (self.questionnaire, self.order, self.name or '')

    def title(self):
        return "(%s) %s" % (self.order, self.name or '')

    def get_absolute_url(self):
        return reverse2("questionnaire", self.questionnaire.pk, self.pk)


class Question(BaseModel):
    question = CharField(max_length=255)
    choices = CharField(max_length=500, blank=True, null=True)
    footnote = CharField(max_length=250, blank=True, null=True)
    answer_type = CharField(max_length=6, choices=(("str", "str"), ("int", "int")))
    section = ForeignKey(Section, related_name="questions", blank=True, null=True)
    order = IntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = [["section", "order"]]

    def __unicode__(self):
        return "%s: %s" % (self.section, self.question)


# UserQuestionnaire and Answer models

class UserQuestionnaire(BaseModel):
    user = ForeignKey(User, related_name="questionnaires", blank=True, null=True)
    session_key = CharField(max_length=255)
    ip_address = CharField(max_length=39)
    user_agent = CharField(max_length=255)
    questionnaire = ForeignKey(Questionnaire, related_name="user_questionnaires", blank=True, null=True)
    created = DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.questionnaire)

    class Meta:
        ordering = ["user", "created"]


class Answer(BaseModel):
    answer = TextField(blank=True)
    question = ForeignKey(Question, related_name="answers", blank="True", null=True)
    user_questionnaire = ForeignKey(UserQuestionnaire, related_name="answers", blank=True, null=True)
    type = IntegerField(null=True, blank=True, default=0)

    def __unicode__(self):
        return "%s - %s" % (self.user_questionnaire, self.answer)

    class Meta:
        ordering = ["question__section__order", "question__order"]


class Thanks(BaseModel):
    title = CharField(max_length=255)
    text = TextField()
    questionnaire = ForeignKey(Questionnaire, related_name="thanks", blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.title

    class Meta:
        verbose_name_plural = "Thanks"


class Header(BaseModel):
    name = CharField(blank=True, max_length=200)
    section = ForeignKey(Section, related_name="headers")

    def __unicode__(self):
        return "%s" % self.name



