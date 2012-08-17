# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AgeMap'
        db.create_table('expressions_agemap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unigene', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('gene_ontology', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('adrenals_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('cerebellum_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('eye_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('gonads_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('heart_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('lung_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('spleen_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('spinal_cord_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('thymus_age_coef', self.gf('django.db.models.fields.FloatField')()),
            ('empirical_meta_analysis_value', self.gf('django.db.models.fields.FloatField')()),
            ('empirical_meta_analysis_p_value', self.gf('django.db.models.fields.FloatField')()),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('expressions', ['AgeMap'])


    def backwards(self, orm):
        
        # Deleting model 'AgeMap'
        db.delete_table('expressions_agemap')


    models = {
        'expressions.agemap': {
            'Meta': {'object_name': 'AgeMap'},
            'adrenals_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'cerebellum_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'empirical_meta_analysis_p_value': ('django.db.models.fields.FloatField', [], {}),
            'empirical_meta_analysis_value': ('django.db.models.fields.FloatField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'eye_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'gene_ontology': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'gonads_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'heart_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lung_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spinal_cord_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'spleen_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'thymus_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'unigene': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'expressions.lin2002': {
            'Meta': {'object_name': 'Lin2002'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '223', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'hap4oe1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hap4oe2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hxk2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_glucose1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'low_glucose2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'expressions.rapamycin': {
            'Meta': {'object_name': 'Rapamycin'},
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fpr1_8_rapamycin_mean': ('django.db.models.fields.FloatField', [], {}),
            'fpr1_8_rapamycin_replicate_1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fpr1_8_rapamycin_replicate_2': ('django.db.models.fields.FloatField', [], {}),
            'fpr1_8_rapamycin_replicate_3': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ly_83583_mean': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ly_83583_replicate_1': ('django.db.models.fields.FloatField', [], {}),
            'ly_83583_replicate_2': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'rapamycin_mean': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rapamycin_replicate_1': ('django.db.models.fields.FloatField', [], {}),
            'rapamycin_replicate_2': ('django.db.models.fields.FloatField', [], {})
        },
        'expressions.rapamycin_protein': {
            'Meta': {'object_name': 'rapamycin_protein'},
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'protein_function': ('django.db.models.fields.CharField', [], {'max_length': '82'})
        },
        'expressions.sip2delta_aging': {
            'Meta': {'object_name': 'sip2delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '172'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
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
