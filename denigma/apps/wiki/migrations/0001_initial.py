# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Page'
        db.create_table('wiki_page', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('wiki', ['Page'])


    def backwards(self, orm):
        
        # Deleting model 'Page'
        db.delete_table('wiki_page')


    models = {
        'wiki.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        }
    }

    complete_apps = ['wiki']
