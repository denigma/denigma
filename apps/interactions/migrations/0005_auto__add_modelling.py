# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Modelling'
        db.create_table('interactions_modelling', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=159, blank=True)),
            ('target', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pmid', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('primary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('interactions', ['Modelling'])


    def backwards(self, orm):
        
        # Deleting model 'Modelling'
        db.delete_table('interactions_modelling')


    models = {
        'interactions.biogrid': {
            'Meta': {'object_name': 'Biogrid'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'biogrid_id_interactor_a': ('django.db.models.fields.IntegerField', [], {}),
            'biogrid_id_interactor_b': ('django.db.models.fields.IntegerField', [], {}),
            'biogrid_interaction_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_interactor_a': ('django.db.models.fields.IntegerField', [], {}),
            'entrez_gene_interactor_b': ('django.db.models.fields.IntegerField', [], {}),
            'experimental_system': ('django.db.models.fields.CharField', [], {'max_length': '29'}),
            'experimental_system_type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'modification': ('django.db.models.fields.CharField', [], {'max_length': '22'}),
            'official_symbol_interactor_a': ('django.db.models.fields.CharField', [], {'max_length': '21'}),
            'official_symbol_interactor_b': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'organism_interactor_a': ('django.db.models.fields.IntegerField', [], {}),
            'organism_interactor_b': ('django.db.models.fields.IntegerField', [], {}),
            'phenotypes': ('django.db.models.fields.CharField', [], {'max_length': '209'}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {}),
            'qualifications': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'source_database': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'synonymns_interactor_a': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'synonyms_interactor_b': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'systematic_name_interactor_a': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'systematic_name_interactor_b': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'throughput': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'interactions.modelling': {
            'Meta': {'object_name': 'Modelling'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interaction_type': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'interactor_a': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'interactor_b': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'interactions.yeastract': {
            'Meta': {'object_name': 'Yeastract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['interactions']
