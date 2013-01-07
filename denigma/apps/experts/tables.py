# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from django_tables2 import tables

from data.templatetags.rendering import markdown

from models import Profile, Collaboration
from templatetags.obfuscation import obfuscate


class ProfileTable(tables.Table):

    def render_user_name(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_work(self, record, value):
        if value:
            return value #[:50] + '...'
        return value

    #def render_email(self, record, value):
    #    return mark_safe('<a href="mailto:%s">%s</a>' % (value, obfuscate(value)))


    class Meta:
        model = Profile
        attrs = {'class': 'paleblue'}
        fields = ('user_name', 'affiliation', 'country', 'work', 'collaboration') #'email'
        exclude = ('id', 'user', 'gender', 'password', 'first_name', 'last_name',
                    'mobile', 'msn', 'street', 'state', 'zip_code', 'birthday', 'website', )


class CollaborationTable(tables.Table):

    def render_project(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_labs(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value.count()))

    def render_members(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), record.members.count()))

    def render_people(self, record, value):
        return mark_safe("; ".join(['<a href="%s">%s</a>' % (member.get_url(), member.password or member.last_name) for member in record.members.all()]))

    def render_description(self, record, value):
        return markdown(value)

    class Meta:
        model = Collaboration
        attrs = {'class': 'paleblue'}
        exclude = ('id',)
        fields = ('project', 'labs', 'members', 'people', 'description')