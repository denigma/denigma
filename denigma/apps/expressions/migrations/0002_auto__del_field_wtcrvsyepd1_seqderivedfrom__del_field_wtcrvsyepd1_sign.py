# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'wtcrvsyepd1.seqderivedfrom'
        db.rename_column('expressions_wtcrvsyepd1', 'seqderivedfrom', 'orf')

        # Deleting field 'wtcrvsyepd1.signal_87974'
        db.rename_column('expressions_wtcrvsyepd1', 'signal_87974', 'al')

        # Deleting field 'wtcrvsyepd1.signal_87973'
        db.rename_column('expressions_wtcrvsyepd1', 'signal_87973', 'dr')

        # Deleting field 'wtcrvsyepd1.cr_yepd'
        db.rename_column('expressions_wtcrvsyepd1', 'cr_yepd', 'dr_al')


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'wtcrvsyepd1.seqderivedfrom'
        raise RuntimeError("Cannot reverse this migration. 'wtcrvsyepd1.seqderivedfrom' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'wtcrvsyepd1.signal_87974'
        raise RuntimeError("Cannot reverse this migration. 'wtcrvsyepd1.signal_87974' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'wtcrvsyepd1.signal_87973'
        raise RuntimeError("Cannot reverse this migration. 'wtcrvsyepd1.signal_87973' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'wtcrvsyepd1.cr_yepd'
        raise RuntimeError("Cannot reverse this migration. 'wtcrvsyepd1.cr_yepd' and its values cannot be restored.")

        # Deleting field 'wtcrvsyepd1.dr'
        db.rename_column('expressions_wtcrvsyepd1', 'dr', 'signal_87973')

        # Deleting field 'wtcrvsyepd1.al'
        db.rename_column('expressions_wtcrvsyepd1', 'al', 'signal_87974')

        # Deleting field 'wtcrvsyepd1.dr_al'
        db.rename_column('expressions_wtcrvsyepd1', 'dr_al', 'dr_al')

        # Deleting field 'wtcrvsyepd1.orf'
        db.rename_column('expressions_wtcrvsyepd1', 'orf', 'seqderivedfrom')


    models = {
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
