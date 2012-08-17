# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Lin2002'
        db.create_table('expressions_lin2002', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=223, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('hap4oe1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hap4oe2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hxk2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('low_glucose1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('low_glucose2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal('expressions', ['Lin2002'])

        # Adding model 'snf4delta_wt'
        db.create_table('expressions_snf4delta_wt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orf', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('fold_change', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=127)),
            ('main_process', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('specific_process', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal('expressions', ['snf4delta_wt'])

        # Adding model 'wt_aging'
        db.create_table('expressions_wt_aging', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orf', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('fold_change', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=146)),
            ('main_process', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('specific_process', self.gf('django.db.models.fields.CharField')(max_length=54, blank=True)),
        ))
        db.send_create_signal('expressions', ['wt_aging'])

        # Adding model 'sip2delta_aging'
        db.create_table('expressions_sip2delta_aging', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orf', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
            ('fold_change', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=172)),
            ('main_process', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('specific_process', self.gf('django.db.models.fields.CharField')(max_length=29, blank=True)),
        ))
        db.send_create_signal('expressions', ['sip2delta_aging'])

        # Adding model 'snf4delta_aging'
        db.create_table('expressions_snf4delta_aging', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orf', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
            ('fold_change', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=155)),
            ('main_process', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('specific_process', self.gf('django.db.models.fields.CharField')(max_length=29, blank=True)),
        ))
        db.send_create_signal('expressions', ['snf4delta_aging'])

        # Adding model 'sip2delta_wt'
        db.create_table('expressions_sip2delta_wt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orf', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('fold_change', self.gf('django.db.models.fields.FloatField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=178)),
            ('main_process', self.gf('django.db.models.fields.CharField')(max_length=56)),
            ('specific_process', self.gf('django.db.models.fields.CharField')(max_length=38, blank=True)),
        ))
        db.send_create_signal('expressions', ['sip2delta_wt'])


    def backwards(self, orm):
        
        # Deleting model 'Lin2002'
        db.delete_table('expressions_lin2002')

        # Deleting model 'snf4delta_wt'
        db.delete_table('expressions_snf4delta_wt')

        # Deleting model 'wt_aging'
        db.delete_table('expressions_wt_aging')

        # Deleting model 'sip2delta_aging'
        db.delete_table('expressions_sip2delta_aging')

        # Deleting model 'snf4delta_aging'
        db.delete_table('expressions_snf4delta_aging')

        # Deleting model 'sip2delta_wt'
        db.delete_table('expressions_sip2delta_wt')


    models = {
        'expressions.lin2002': {
            'Meta': {'object_name': 'Lin2002'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '223', 'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'hap4oe1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hap4oe2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hxk2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_glucose1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'low_glucose2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'expressions.sip2delta_aging': {
            'Meta': {'object_name': 'sip2delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '172'}),
            'fold_change': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'})
        },
        'expressions.sip2delta_wt': {
            'Meta': {'object_name': 'sip2delta_wt'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '178'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '38', 'blank': 'True'})
        },
        'expressions.snf4delta_aging': {
            'Meta': {'object_name': 'snf4delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '155'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'})
        },
        'expressions.snf4delta_wt': {
            'Meta': {'object_name': 'snf4delta_wt'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'expressions.wt_aging': {
            'Meta': {'object_name': 'wt_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '146'}),
            'fold_change': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'})
        },
        'expressions.wtcrvsyepd1': {
            'Meta': {'object_name': 'wtcrvsyepd1'},
            'al': ('django.db.models.fields.FloatField', [], {}),
            'dr': ('django.db.models.fields.FloatField', [], {}),
            'dr_al': ('django.db.models.fields.FloatField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['expressions']
