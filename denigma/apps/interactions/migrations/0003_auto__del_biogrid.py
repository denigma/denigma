# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Biogrid'
        db.delete_table('interactions_biogrid')


    def backwards(self, orm):
        
        # Adding model 'Biogrid'
        db.create_table('interactions_biogrid', (
            ('entrez_gene_interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('entrez_gene_interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=37)),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('pubmed_id', self.gf('django.db.models.fields.IntegerField')()),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=22)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('biogrid_id_interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('biogrid_id_interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('qualifications', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('phenotypes', self.gf('django.db.models.fields.CharField')(max_length=209)),
            ('synonymns_interactor_a', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('organism_interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('official_symbol_interactor_a', self.gf('django.db.models.fields.CharField')(max_length=21)),
            ('official_symbol_interactor_b', self.gf('django.db.models.fields.CharField')(max_length=31)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('organism_interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('biogrid_interaction_id', self.gf('django.db.models.fields.IntegerField')()),
            ('experimental_system', self.gf('django.db.models.fields.CharField')(max_length=29)),
            ('synonyms_interactor_b', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('systematic_name_interactor_a', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('systematic_name_interactor_b', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('throughput', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('interactions', ['Biogrid'])


    models = {
        'interactions.yeastract': {
            'Meta': {'object_name': 'Yeastract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['interactions']
