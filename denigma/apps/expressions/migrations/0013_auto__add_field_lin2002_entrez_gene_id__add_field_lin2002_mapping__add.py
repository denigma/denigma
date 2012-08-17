# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Lin2002.entrez_gene_id'
        db.add_column('expressions_lin2002', 'entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Lin2002.mapping'
        db.add_column('expressions_lin2002', 'mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'snf4delta_wt.entrez_gene_id'
        db.add_column('expressions_snf4delta_wt', 'entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'snf4delta_wt.mapping'
        db.add_column('expressions_snf4delta_wt', 'mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'wt_aging.entrez_gene_id'
        db.add_column('expressions_wt_aging', 'entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'wt_aging.mapping'
        db.add_column('expressions_wt_aging', 'mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'sip2delta_aging.entrez_gene_id'
        db.add_column('expressions_sip2delta_aging', 'entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'sip2delta_aging.mapping'
        db.add_column('expressions_sip2delta_aging', 'mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'snf4delta_aging.entrez_gene_id'
        db.add_column('expressions_snf4delta_aging', 'entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'snf4delta_aging.mapping'
        db.add_column('expressions_snf4delta_aging', 'mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'sip2delta_wt.entrez_gene_id'
        db.add_column('expressions_sip2delta_wt', 'entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'sip2delta_wt.mapping'
        db.add_column('expressions_sip2delta_wt', 'mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Lin2002.entrez_gene_id'
        db.delete_column('expressions_lin2002', 'entrez_gene_id')

        # Deleting field 'Lin2002.mapping'
        db.delete_column('expressions_lin2002', 'mapping')

        # Deleting field 'snf4delta_wt.entrez_gene_id'
        db.delete_column('expressions_snf4delta_wt', 'entrez_gene_id')

        # Deleting field 'snf4delta_wt.mapping'
        db.delete_column('expressions_snf4delta_wt', 'mapping')

        # Deleting field 'wt_aging.entrez_gene_id'
        db.delete_column('expressions_wt_aging', 'entrez_gene_id')

        # Deleting field 'wt_aging.mapping'
        db.delete_column('expressions_wt_aging', 'mapping')

        # Deleting field 'sip2delta_aging.entrez_gene_id'
        db.delete_column('expressions_sip2delta_aging', 'entrez_gene_id')

        # Deleting field 'sip2delta_aging.mapping'
        db.delete_column('expressions_sip2delta_aging', 'mapping')

        # Deleting field 'snf4delta_aging.entrez_gene_id'
        db.delete_column('expressions_snf4delta_aging', 'entrez_gene_id')

        # Deleting field 'snf4delta_aging.mapping'
        db.delete_column('expressions_snf4delta_aging', 'mapping')

        # Deleting field 'sip2delta_wt.entrez_gene_id'
        db.delete_column('expressions_sip2delta_wt', 'entrez_gene_id')

        # Deleting field 'sip2delta_wt.mapping'
        db.delete_column('expressions_sip2delta_wt', 'mapping')


    models = {
        'expressions.lin2002': {
            'Meta': {'object_name': 'Lin2002'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '223', 'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'hap4oe1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hap4oe2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hxk2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_glucose1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'low_glucose2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'expressions.sip2delta_aging': {
            'Meta': {'object_name': 'sip2delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '172'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'})
        },
        'expressions.sip2delta_wt': {
            'Meta': {'object_name': 'sip2delta_wt'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '178'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '38', 'blank': 'True'})
        },
        'expressions.snf4delta_aging': {
            'Meta': {'object_name': 'snf4delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '155'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'})
        },
        'expressions.snf4delta_wt': {
            'Meta': {'object_name': 'snf4delta_wt'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'expressions.wt_aging': {
            'Meta': {'object_name': 'wt_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '146'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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
