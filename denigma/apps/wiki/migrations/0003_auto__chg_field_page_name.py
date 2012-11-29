# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Page.name'
        db.alter_column('wiki_page', 'name', self.gf('django.db.models.fields.CharField')(max_length=250, primary_key=True))

    def backwards(self, orm):

        # Changing field 'Page.name'
        db.alter_column('wiki_page', 'name', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True))

    models = {
        'wiki.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['wiki.Tag']", 'symmetrical': 'False'})
        },
        'wiki.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        }
    }

    complete_apps = ['wiki']