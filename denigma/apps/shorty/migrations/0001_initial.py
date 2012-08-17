# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SourceURL'
        db.create_table('shorty_sourceurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=250)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('admin_key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40, db_index=True)),
        ))
        db.send_create_signal('shorty', ['SourceURL'])

        # Adding model 'ShortyURL'
        db.create_table('shorty_shortyurl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shorty_urls', to=orm['shorty.SourceURL'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('notify', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('shorty', ['ShortyURL'])

        # Adding model 'Visit'
        db.create_table('shorty_visit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('shorty', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visits', to=orm['shorty.ShortyURL'])),
            ('user_agent_string', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('shorty', ['Visit'])


    def backwards(self, orm):
        # Deleting model 'SourceURL'
        db.delete_table('shorty_sourceurl')

        # Deleting model 'ShortyURL'
        db.delete_table('shorty_shortyurl')

        # Deleting model 'Visit'
        db.delete_table('shorty_visit')


    models = {
        'shorty.shortyurl': {
            'Meta': {'object_name': 'ShortyURL'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notify': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shorty_urls'", 'to': "orm['shorty.SourceURL']"})
        },
        'shorty.sourceurl': {
            'Meta': {'object_name': 'SourceURL'},
            'admin_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '250'})
        },
        'shorty.visit': {
            'Meta': {'object_name': 'Visit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'shorty': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visits'", 'to': "orm['shorty.ShortyURL']"}),
            'user_agent_string': ('django.db.models.fields.TextField', [], {}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['shorty']