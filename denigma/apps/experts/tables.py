# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from django_tables2 import tables

from models import Profile
from templatetags.obfuscation import obfuscate


class ProfileTable(tables.Table):

    def render_user_name(self, record, value):
        return mark_safe('<a href="%s">%s</a>' % (record.get_absolute_url(), value))

    def render_email(self, record, value):
        return mark_safe('<a href="mailto:%s">%s</a>' % (value, obfuscate(value)))

    class Meta:
        model = Profile
        attrs = {'class': 'paleblue'}
        fields = ('user_name', 'affliation', 'country', 'email', 'website', 'collaboration')
        exclude = ('id', 'user', 'gender', 'password', 'first_name', 'last_name',
                   'work', 'mobile', 'msn', 'street', 'state', 'zip_code', 'birthday')
