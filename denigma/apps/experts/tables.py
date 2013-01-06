# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from django_tables2 import tables

from models import Profile, Collaboration
from templatetags.obfuscation import obfuscate


class ProfileTable(tables.Table):

    def render_user_name(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_email(self, record, value):
        return mark_safe('<a href="mailto:%s">%s</a>' % (value, obfuscate(value)))


    class Meta:
        model = Profile
        attrs = {'class': 'paleblue'}
        fields = ('user_name', 'affiliation', 'country', 'email', 'website', 'collaboration')
        exclude = ('id', 'user', 'gender', 'password', 'first_name', 'last_name',
                   'work', 'mobile', 'msn', 'street', 'state', 'zip_code', 'birthday')


class CollaborationTable(tables.Table):

    def render_project(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_labs(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value.count()))

    def render_members(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value.count()))

    def render_id(self, record, value):
        return mark_safe("; ".join(['<a href="%s">%s</a>' % (member.get_absolute_url(), member.user_name.split(' ')[-1]) for member in record.members.all()]))

    class Meta:
        model = Collaboration
        attrs = {'class': 'paleblue'}
        #exclude = ('id',)
        fields = ('project', 'labs', 'members', 'id')