# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Message'
        db.create_table('chat_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('server', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('join_or_leave', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('chat', ['Message'])


    def backwards(self, orm):
        # Deleting model 'Message'
        db.delete_table('chat_message')


    models = {
        'chat.message': {
            'Meta': {'ordering': "('time',)", 'object_name': 'Message'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_or_leave': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'server': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['chat']
