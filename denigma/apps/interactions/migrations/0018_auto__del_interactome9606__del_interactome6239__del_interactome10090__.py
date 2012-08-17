# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Interactome9606'
        db.delete_table('interactions_interactome9606')

        # Deleting model 'Interactome6239'
        db.delete_table('interactions_interactome6239')

        # Deleting model 'Interactome10090'
        db.delete_table('interactions_interactome10090')

        # Deleting model 'Interactome7227'
        db.delete_table('interactions_interactome7227')

        # Deleting model 'Interactome4932'
        db.delete_table('interactions_interactome4932')


    def backwards(self, orm):
        
        # Adding model 'Interactome9606'
        db.create_table('interactions_interactome9606', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=251, blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=49, blank=True)),
            ('pmid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome9606'])

        # Adding model 'Interactome6239'
        db.create_table('interactions_interactome6239', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=46, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=89)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('pmid', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome6239'])

        # Adding model 'Interactome10090'
        db.create_table('interactions_interactome10090', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=38, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=73)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.CharField')(max_length=240, blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=159, blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('pmid', self.gf('django.db.models.fields.CharField')(max_length=115, blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome10090'])

        # Adding model 'Interactome7227'
        db.create_table('interactions_interactome7227', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=89)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('pmid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome7227'])

        # Adding model 'Interactome4932'
        db.create_table('interactions_interactome4932', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=46, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=115)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=49, blank=True)),
            ('pmid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome4932'])


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
            'qualifications': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'source_database': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'synonymns_interactor_a': ('django.db.models.fields.TextField', [], {}),
            'synonyms_interactor_b': ('django.db.models.fields.TextField', [], {}),
            'systematic_name_interactor_a': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'systematic_name_interactor_b': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'throughput': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
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
