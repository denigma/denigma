# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Biogrid'
        db.create_table('interactions_biogrid', (
            ('biogrid_interaction_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('entrez_gene_interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('entrez_gene_interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('biogrid_id_interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('biogrid_id_interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('systematic_name_interactor_a', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('systematic_name_interactor_b', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('official_symbol_interactor_a', self.gf('django.db.models.fields.CharField')(max_length=21)),
            ('official_symbol_interactor_b', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('synonymns_interactor_a', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('synonyms_interactor_b', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('experimental_system', self.gf('django.db.models.fields.CharField')(max_length=29)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('pubmed_id', self.gf('django.db.models.fields.IntegerField')()),
            ('organism_interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('organism_interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('throughput', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=22)),
            ('phenotypes', self.gf('django.db.models.fields.CharField')(max_length=209)),
            ('qualifications', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal('interactions', ['Biogrid'])


    def backwards(self, orm):
        
        # Deleting model 'Biogrid'
        db.delete_table('interactions_biogrid')


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
        'interactions.yeastract': {
            'Meta': {'object_name': 'Yeastract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['interactions']
