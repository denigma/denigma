# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Entity'
        db.create_table('ontology_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('ontology', ['Entity'])

        # Adding model 'Relation'
        db.create_table('ontology_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_relations', to=orm['ontology.Entity'])),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relations', to=orm['ontology.Entity'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source_relations', to=orm['ontology.Entity'])),
        ))
        db.send_create_signal('ontology', ['Relation'])


    def backwards(self, orm):
        # Deleting model 'Entity'
        db.delete_table('ontology_entity')

        # Deleting model 'Relation'
        db.delete_table('ontology_relation')


    models = {
        'ontology.entity': {
            'Meta': {'object_name': 'Entity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'ontology.relation': {
            'Meta': {'object_name': 'Relation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_relations'", 'to': "orm['ontology.Entity']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_relations'", 'to': "orm['ontology.Entity']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relations'", 'to': "orm['ontology.Entity']"})
        }
    }

    complete_apps = ['ontology']