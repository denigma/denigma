# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'DisconnectedId'
        db.delete_table('annotations_disconnectedid')

        # Adding model 'DiscontinuedId'
        db.create_table('annotations_discontinuedid', (
            ('discontinued_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('annotations', ['DiscontinuedId'])


    def backwards(self, orm):
        
        # Adding model 'DisconnectedId'
        db.create_table('annotations_disconnectedid', (
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')()),
            ('disconnected_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal('annotations', ['DisconnectedId'])

        # Deleting model 'DiscontinuedId'
        db.delete_table('annotations_discontinuedid')


    models = {
        'annotations.discontinuedid': {
            'Meta': {'object_name': 'DiscontinuedId'},
            'discontinued_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['annotations']
