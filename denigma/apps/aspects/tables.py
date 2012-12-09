import django_tables2 as tables
from django.utils.safestring import mark_safe

from models import Rank, Grade, Title


class Table(tables.Table):

    def render_symbol(self, value, record):
        return mark_safe('<center><img src="%s" alt="%s" width="25" height="25"></center>' % (value.url, value.name))


class RankTable(Table):

    def render_name(self, value, record):
        return mark_safe('<a href="/aspects/research/rank/%s">%s</a>' % (record.name, value))

    class Meta:
        model = Rank
        attrs = {"class": "paleblue"}
        exclude = ('id', 'type', 'hierarchy_ptr')


class GradeTable(Table):

    def render_name(self, value, record):
        return mark_safe('<a href="/aspects/programming/grade/%s">%s</a>' % (record.name, value))

    class Meta:
        model = Grade
        attrs = {"class": "paleblue"}
        exclude = ('id', 'type', 'hierarchy_ptr')


class TitleTable(tables.Table):

    def render_name(self, value, record):
        return mark_safe('<a href="/aspects/design/title/%s">%s</a>' % (record.name, value))

    class Meta:
        model = Title
        attrs = {"class": "paleblue"}
        exclude = ('id', 'type', 'hierarchy_ptr')