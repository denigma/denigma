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
            ('biogrid_interaction_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('experimental_system', self.gf('django.db.models.fields.CharField')(max_length=29)),
            ('synonyms_interactor_b', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('systematic_name_interactor_a', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('systematic_name_interactor_b', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('throughput', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('interactions', ['Biogrid'])


    models = {
        'interactions.mirecord': {
            'Meta': {'object_name': 'miRecord'},
            'additional_note': ('django.db.models.fields.CharField', [], {'max_length': '141', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mirna_mature_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'mirna_regulation': ('django.db.models.fields.CharField', [], {'max_length': '66', 'blank': 'True'}),
            'mirna_regulation_site': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'mirna_species': ('django.db.models.fields.CharField', [], {'max_length': '37', 'blank': 'True'}),
            'mutation_target_region': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'mutation_target_site': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'original_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_description_inter_site': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_description_mutation_region': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_description_mutation_site': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'post_mutation_method': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'post_mutation_method_site': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {}),
            'reporter_link_element1': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'reporter_link_element2': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'reporter_target_gene_region': ('django.db.models.fields.CharField', [], {'max_length': '26', 'blank': 'True'}),
            'reporter_target_site': ('django.db.models.fields.CharField', [], {'max_length': '26', 'blank': 'True'}),
            'target_gene_mrna_level': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'target_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '44', 'blank': 'True'}),
            'target_gene_refseq_acc': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'target_gene_species_common': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'target_gene_species_scientific': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'target_site_number': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'target_site_position': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'test_method_inter': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'test_method_inter_site': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'})
        },
        'interactions.modelling': {
            'Meta': {'object_name': 'Modelling'},
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interaction_type': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'interactor_a': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'interactor_b': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
