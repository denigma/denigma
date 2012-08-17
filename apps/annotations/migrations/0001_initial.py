# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DisconnectedId'
        db.create_table('annotations_disconnectedid', (
            ('disconnected_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('annotations', ['DisconnectedId'])


    def backwards(self, orm):
        
        # Deleting model 'DisconnectedId'
        db.delete_table('annotations_disconnectedid')


    models = {
        'annotations.disconnectedid': {
            'Meta': {'object_name': 'DisconnectedId'},
            'disconnected_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['annotations']
