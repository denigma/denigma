# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SGD_features'
        db.create_table('annotations_sgd_features', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sgd_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('feature_type', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('feature_qualifier', self.gf('django.db.models.fields.CharField')(max_length=22, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=63, blank=True)),
            ('parent_feature_name', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('secondary_sgd_id', self.gf('django.db.models.fields.CharField')(max_length=54, blank=True)),
            ('chromosome', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('start_coordinate', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('stop_coordinate', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('strand', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('genetic_position', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('coordinate_version', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('sequence_version', self.gf('django.db.models.fields.CharField')(max_length=43)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('annotations', ['SGD_features'])

        # Adding model 'SGD_gene_association'
        db.create_table('annotations_sgd_gene_association', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sgd_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('with_or_from', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('go_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('evidence', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('other_ids', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=72)),
            ('orf', self.gf('django.db.models.fields.CharField')(max_length=54)),
            ('date', self.gf('django.db.models.fields.IntegerField')()),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['SGD_gene_association'])


    def backwards(self, orm):
        
        # Deleting model 'SGD_features'
        db.delete_table('annotations_sgd_features')

        # Deleting model 'SGD_gene_association'
        db.delete_table('annotations_sgd_gene_association')


    models = {
        'annotations.candidate': {
            'Meta': {'object_name': 'Candidate', 'db_table': "u'Candidate'"},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'fly_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'fly_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'human_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'human_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mouse_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'mouse_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'p-Value'", 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rat_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'rat_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            's': ('django.db.models.fields.IntegerField', [], {}),
            'seed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specificity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            't': ('django.db.models.fields.IntegerField', [], {}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'worm_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'worm_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'yeast_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'yeast_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'annotations.discontinuedid': {
            'Meta': {'object_name': 'DiscontinuedId'},
            'discontinued_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.entrez': {
            'Meta': {'object_name': 'Entrez'},
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'full_name_from_nomenclature_autority': ('django.db.models.fields.CharField', [], {'max_length': '251', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'hgnc': ('django.db.models.fields.IntegerField', [], {}),
            'hprd': ('django.db.models.fields.IntegerField', [], {}),
            'imgt_gene_db': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'mgi': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'mim': ('django.db.models.fields.IntegerField', [], {}),
            'mirbase': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'ratmap': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'rgd': ('django.db.models.fields.IntegerField', [], {}),
            'symbol_from_nomeclature_authority': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        },
        'annotations.go': {
            'Meta': {'object_name': 'GO'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'go_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'go_term': ('django.db.models.fields.CharField', [], {'max_length': '193'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pmid': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'qualifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.sgd_features': {
            'Meta': {'object_name': 'SGD_features'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'chromosome': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'coordinate_version': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'feature_qualifier': ('django.db.models.fields.CharField', [], {'max_length': '22', 'blank': 'True'}),
            'feature_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'genetic_position': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_feature_name': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'secondary_sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'}),
            'sequence_version': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
            'sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_coordinate': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'stop_coordinate': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'strand': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'annotations.sgd_gene_association': {
            'Meta': {'object_name': 'SGD_gene_association'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'date': ('django.db.models.fields.IntegerField', [], {}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '72'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'go_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '54'}),
            'other_ids': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'with_or_from': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        }
    }

    complete_apps = ['annotations']
