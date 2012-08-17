# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Gendr'
        db.create_table('datasets_gendr', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
            ('observation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pubmed_id', self.gf('django.db.models.fields.CharField')(max_length=87, blank=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=27, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('datasets', ['Gendr'])


    def backwards(self, orm):
        
        # Deleting model 'Gendr'
        db.delete_table('datasets_gendr')


    models = {
        'datasets.gendr': {
            'Meta': {'object_name': 'Gendr'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '87', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['datasets']
