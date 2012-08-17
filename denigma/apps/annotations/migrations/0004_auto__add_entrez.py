# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Entrez'
        db.create_table('annotations_entrez', (
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('symbol_from_nomeclature_authority', self.gf('django.db.models.fields.CharField')(max_length=29, blank=True)),
            ('full_name_from_nomenclature_autority', self.gf('django.db.models.fields.CharField')(max_length=251, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('mirbase', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('mgi', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('hgnc', self.gf('django.db.models.fields.IntegerField')()),
            ('mim', self.gf('django.db.models.fields.IntegerField')()),
            ('hprd', self.gf('django.db.models.fields.IntegerField')()),
            ('rgd', self.gf('django.db.models.fields.IntegerField')()),
            ('ratmap', self.gf('django.db.models.fields.IntegerField')()),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('imgt_gene_db', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('annotations', ['Entrez'])


    def backwards(self, orm):
        
        # Deleting model 'Entrez'
        db.delete_table('annotations_entrez')


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
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'hgnc': ('django.db.models.fields.IntegerField', [], {}),
            'hprd': ('django.db.models.fields.IntegerField', [], {}),
            'imgt_gene_db': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'mgi': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'mim': ('django.db.models.fields.IntegerField', [], {}),
            'mirbase': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'ratmap': ('django.db.models.fields.IntegerField', [], {}),
            'rgd': ('django.db.models.fields.IntegerField', [], {}),
            'symbol_from_nomeclature_authority': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        }
    }

    complete_apps = ['annotations']
