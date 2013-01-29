from django.utils.safestring import mark_safe

import django_tables2 as tables

from models import Todo

from blog.templatetags.hyperlink import hyper
from blog.templatetags.crosslink import recross


priority_colors = {'Very high':'purple', 'High': 'red', 'Medium':'orange', 'Low':'green'}


class TodoTable(tables.Table):

    def render_title(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_description(self, record, value):
        return mark_safe(recross(hyper(value)))

    def render_priority(self, record, value):
        return mark_safe('<span style="color:%s">%s</span>' % (priority_colors[value], value))

    def render_creator(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url, value))

    def render_quest(self, record, value):
        return mark_safe('<a href="/quests/todo/%s">Quest it</a>' % record.pk)



    class Meta:
        model = Todo
        attrs = {"class": "paleblue"}
        exclude = ('id',)
        fields = ('title', 'description', 'priority', 'created', 'updated', 'start_date', 'stop_date', 'done', 'creator', 'quest')
