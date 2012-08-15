# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Candidate'
        db.create_table(u'Candidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('gene_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('t', self.gf('django.db.models.fields.IntegerField')()),
            ('s', self.gf('django.db.models.fields.IntegerField')()),
            ('specificity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('p_value', self.gf('django.db.models.fields.FloatField')(null=True, db_column='p-Value', blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('seed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('yeast_homolog_id', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('worm_homolog_id', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('fly_homolog_id', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('mouse_homolog_id', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('rat_homolog_id', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('human_homolog_id', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('yeast_homolog_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('worm_homolog_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('fly_homolog_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('mouse_homolog_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('rat_homolog_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
            ('human_homolog_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True)),
        ))
        db.send_create_signal('annotations', ['Candidate'])


    def backwards(self, orm):
        
        # Deleting model 'Candidate'
        db.delete_table(u'Candidate')


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
        }
    }

    complete_apps = ['annotations']
