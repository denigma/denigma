# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'GenDR'
        db.delete_table('datasets_gendr')


    def backwards(self, orm):
        
        # Adding model 'GenDR'
        db.create_table('datasets_gendr', (
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=27, blank=True)),
            ('observation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('pubmed_id', self.gf('django.db.models.fields.CharField')(max_length=87, blank=True)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
        ))
        db.send_create_signal('datasets', ['GenDR'])


    models = {
        
    }

    complete_apps = ['datasets']
