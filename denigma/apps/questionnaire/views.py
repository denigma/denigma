# Create your views here.
from operator import itemgetter
from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser, User
from forms import SectionForm
from models import Questionnaire, UserQuestionnaire, Section, Answer

from utils import DefaultOrderedDict, defdict_to_odict, redir
from mcbv.detail import DetailView
from mcbv.edit import FormView
from mcbv.list_custom import ListView, ListRelated


class Questionnaires(ListView):
    list_model = Questionnaire
    template_name = "questionnaire/questionnaires.html"


class UserQuests(ListRelated):
    detail_model = Questionnaire
    list_model = UserQuestionnaire
    related_name = "user_questionnaires"
    template_name = "questionnaire/user-quests.html"


class UserQuest(DetailView):
    detail_model = UserQuestionnaire
    template_name = "questionnaire/user-quest.html"


class QuestStates(DetailView):
    detail_model = Questionnaire
    template_name = "questionnaire/quest-stats.html"

    def stats(self):
        user_quests = UserQuestionnaire.obj.filter(questionnaire=self.detail_object)
        d = DefaultOrderedDict
        # quests    sections    questions   answers:nums
        quests = d(lambda:d(lambda:d(lambda:d(int))))

        for user_quest in user_quests:
            quest = user_quest.questionnaire.name

            # add each answer in user questionnaire to respective sections sub-dict, add to counter
            for answer in user_quest.answers.all():
                question = answer.question
                answer = answer.answer
                q = question.question
                section = question.section.name

                quests[quest][section][q][answer] += 1

        # Sort to have most frequent answers first
        for quest in quests.values():
            for section in quest.values():
                for name, question in section.items():
                    answers = sorted(question.items(), key=itemgetter(1), reverse=True)
                    section[name] = OrderedDict(answers)
        print(quests)
        return defdict_to_odict(quests)

class QuestStats(DetailView):
    detail_model  = Questionnaire
    template_name = "questionnaire/quest-stats.html"

    def stats(self):
        user_quests = UserQuestionnaire.obj.filter(questionnaire=self.detail_object)
        d           = DefaultOrderedDict
        #             quests    sections  questions answers:nums
        quests      = d( lambda:d( lambda:d( lambda:d(int) ) ) )

        for user_quest in user_quests:
            quest = user_quest.questionnaire.name

            # add each answer in user questionnaire to respective sections sub-dict, add to counter
            for answer in user_quest.answers.all():
                question = answer.question
                answer   = answer.answer
                q        = question.question
                section  = question.section.name

                quests[quest][section][q][answer] += 1

        # sort to have most frequent answers first
        for quest in quests.values():
            for section in quest.values():
                for name, question in section.items():
                    answers       = sorted(question.items(), key=itemgetter(1), reverse=True)
                    section[name] = OrderedDict(answers)

        return defdict_to_odict(quests)

class ViewQuestionnaire(ListRelated, FormView):
    detail_model = Questionnaire
    list_model = Section
    related_name = "sections"
    form_class = SectionForm
    template_name = "questionnaire/quest.html"

    def get_section(self):
        self.snum = int(self.kwargs.get("section", 1))
        return self.get_list_queryset()[self.snum-1]

    def get_form_kwargs(self):
        kwargs = super(ViewQuestionnaire, self).get_form_kwargs()
        return dict(kwargs, section=self.get_section())

    def form_valid(self, form):
        """Create user answer records using form data."""
        stotal = self.get_list_queryset().count()
        quest = self.get_detail_object()
        if isinstance(self.user, AnonymousUser):
            self.user = User.objects.get(username='Anonymous')
        uquest = UserQuestionnaire.obj.get_or_create(questionnaire=quest, user=self.user)[0]
        section = self.get_section()

        for order, value in form.cleaned_data.items():
            question = section.questions.get(order=int(order))
            answer = Answer.obj.get_or_create(user_questionnaire=uquest, question=question)[0]

        # Redirect to the next section or to 'done' page:
        if self.snum >= stotal: return redir("done")
        else: return redir(quest.get_absolute_url(self.snum+1))
