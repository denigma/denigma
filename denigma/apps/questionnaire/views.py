from operator import itemgetter
from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser, User
from django.views.generic import DetailView
from forms import SectionForm, QuestForm
from models import Questionnaire, UserQuestionnaire, Section, Answer, Thanks

from utils import DefaultOrderedDict, defdict_to_odict, redir
from mcbv.detail import DetailView
from mcbv.edit import FormView
from mcbv.list_custom import ListView, ListRelated

from track.utils import get_ip

from data import get


class Questionnaires(ListView):
    list_model = Questionnaire
    template_name = "questionnaire/questionnaires.html"

    def get_context_data(self, **kwargs):
        context = super(Questionnaires, self).get_context_data(**kwargs)
        context['entry'] = get("Questionnaire")
        return context

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



class ViewQuestionnaire(ListRelated, FormView):
    detail_model = Questionnaire
    list_model = Section
    related_name = "sections"
    form_class = SectionForm
    template_name = "questionnaire/quest.html"

    def get_section(self):
        self.snum = int(self.kwargs.get("section", 1))
        return self.get_list_queryset()[self.snum-1]

    def get_context_data(self, **kwargs):
        context = super(ViewQuestionnaire, self).get_context_data(**kwargs)
        context['current'] = self.snum
        return context

    def get_form_kwargs(self):
        kwargs = super(ViewQuestionnaire, self).get_form_kwargs()
        return dict(kwargs, section=self.get_section())

    def form_valid(self, form):
        """Create user answer records using form data."""
        stotal = self.get_list_queryset().count()
        quest = self.get_detail_object()

        ip_address = get_ip(self.request)
        user_agent = unicode(self.request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')
        if hasattr(self.request, 'session') and self.request.session.session_key:
            session_key = self.request.session.session_key
        else:
            session_key = '%s:%s' % (ip_address, user_agent)

        if isinstance(self.user, AnonymousUser):
            self.user = User.objects.get(username='Anonymous')
            uquest = UserQuestionnaire.obj.get_or_create(questionnaire=quest,
                                                         user=self.user,
                                                         session_key=session_key,
                                                         ip_address=ip_address,
                                                         user_agent=user_agent)[0]
        else:
            uquest = UserQuestionnaire.obj.get_or_create(questionnaire=quest,
                                                         user=self.user,
                                                         session_key=session_key,
                                                         ip_address=ip_address,
                                                         user_agent=user_agent)[0]

        section = self.get_section()

        if not "Stages" in section.name:
            for order, value in form.cleaned_data.items():
                question = section.questions.get(order=int(order))
                answer = Answer.obj.get_or_create(user_questionnaire=uquest, question=question)[0]
                answer.update(answer=value)
        else:
            for order, value in form.cleaned_data.items():
                if 'help' == order.split('-')[-1]:
                    type = 1
                else:
                    type = 2
                question = section.questions.get(order=int(order.split('-')[0]))
                answer = Answer.obj.create(user_questionnaire=uquest, question=question)
                answer.update(answer=value, type=type)

        # Redirect to the next section or to 'done' page:
        if self.snum >= stotal: return redir("done")
        else: return redir(quest.get_absolute_url(self.snum+1))


class ViewQuests(ViewQuestionnaire):
    form_class = QuestForm
    template_name = "questionnaire/quests.html"
    detail_queryset = Questionnaire.objects.all()

    def dispatch(self, request, *args, **kwargs):
        print args, kwargs
        if not 'dpk' in self.kwargs:
            kwargs['dpk'] = u'2'
        return super(ViewQuests, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Create user answer records using form data."""
        stotal = self.get_list_queryset().count()
        quest = self.get_detail_object()

        ip_address = get_ip(self.request)
        user_agent = unicode(self.request.META.get('HTTP_USER_AGENT', '')[:255], errors='ignore')
        if hasattr(self.request, 'session') and self.request.session.session_key:
            session_key = self.request.session.session_key
        else:
            session_key = '%s:%s' % (ip_address, user_agent)

        if isinstance(self.user, AnonymousUser):
            self.user = User.objects.get(username='Anonymous')
            uquest = UserQuestionnaire.obj.get_or_create(questionnaire=quest,
                user=self.user,
                session_key=session_key,
                ip_address=ip_address,
                user_agent=user_agent)[0]
        else:
            uquest = UserQuestionnaire.obj.get_or_create(questionnaire=quest,
                user=self.user,
                session_key=session_key,
                ip_address=ip_address,
                user_agent=user_agent)[0]

        for section in form.questionnaire.sections.all():
            #section = self.get_section()
            section_name = section.name.lower()
            #print form.cleaned_data.items()

            if not "Stages" in section.name:

                for order, value in form.cleaned_data.items():

                    if section_name in order.lower():
                        question = section.questions.get(order=int(order.split('::')[1]))
                        answer = Answer.obj.get_or_create(user_questionnaire=uquest, question=question)[0]
                        answer.update(answer=value)

            else:
                for order, value in form.cleaned_data.items():
                    if section_name in order.lower():
                        if 'help' == order.split('::')[1].split('-')[1]:
                            type = 1
                        else:
                            type = 2
                        question = section.questions.get(order=int(order.split('::')[1].split('-')[0]))
                        answer = Answer.obj.create(user_questionnaire=uquest, question=question) #[0]
                        answer.update(answer=value, type=type)


        thanks = form.questionnaire.thanks.all()
        if thanks:
            pk = thanks[0].pk
        else:
            pk = 1
        return redir("thanks", pk)


class ThankYouView(DetailView):
    template_name = "questionnaire/thanks.html"
    model = Thanks
    thanks = Thanks.objects.all()
    if thanks:
        detail_model = thanks[0]