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


    def backwards(self, orm):
        
        # Deleting model 'Lin2002'
        db.delete_table('expressions_lin2002')


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
