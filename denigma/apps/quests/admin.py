from django.contrib import admin
from models import Question, Answer

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
