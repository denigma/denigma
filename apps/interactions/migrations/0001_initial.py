# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Yeastract'
        db.create_table('interactions_yeastract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tf', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('interactions', ['Yeastract'])


    def backwards(self, orm):
        
        # Deleting model 'Yeastract'
        db.delete_table('interactions_yeastract')


    models = {
        'interactions.yeastract': {
            'Meta': {'object_name': 'Yeastract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['interactions']
