# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'wtcrvsyepd1'
        db.create_table('expressions_wtcrvsyepd1', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('signal_87973', self.gf('django.db.models.fields.FloatField')()),
            ('signal_87974', self.gf('django.db.models.fields.FloatField')()),
            ('cr_yepd', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('seqderivedfrom', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('expressions', ['wtcrvsyepd1'])


    def backwards(self, orm):
        
        # Deleting model 'wtcrvsyepd1'
        db.delete_table('expressions_wtcrvsyepd1')


    models = {
        'expressions.wtcrvsyepd1': {
            'Meta': {'object_name': 'wtcrvsyepd1'},
            'cr_yepd': ('django.db.models.fields.FloatField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seqderivedfrom': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'signal_87973': ('django.db.models.fields.FloatField', [], {}),
            'signal_87974': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['expressions']
