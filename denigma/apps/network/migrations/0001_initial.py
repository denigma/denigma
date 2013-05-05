# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Analysis'
        db.create_table('network_analysis', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['annotations.Species'])),
        ))
        db.send_create_signal('network', ['Analysis'])

        # Adding model 'Enrichment'
        db.create_table('network_enrichment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('t', self.gf('django.db.models.fields.IntegerField')()),
            ('s', self.gf('django.db.models.fields.IntegerField')()),
            ('r', self.gf('django.db.models.fields.FloatField')()),
            ('pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('genes', self.gf('django.db.models.fields.TextField')()),
            ('analysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.Analysis'])),
        ))
        db.send_create_signal('network', ['Enrichment'])

        # Adding model 'Candidate'
        db.create_table('network_candidate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('gene_name', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('t', self.gf('django.db.models.fields.IntegerField')()),
            ('s', self.gf('django.db.models.fields.IntegerField')()),
            ('specificity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('p_value', self.gf('django.db.models.fields.FloatField')(null=True, db_column='p-Value', blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['annotations.Species'], null=True, blank=True)),
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
            ('dr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('analysis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['network.Analysis'])),
        ))
        db.send_create_signal('network', ['Candidate'])


    def backwards(self, orm):
        # Deleting model 'Analysis'
        db.delete_table('network_analysis')

        # Deleting model 'Enrichment'
        db.delete_table('network_enrichment')

        # Deleting model 'Candidate'
        db.delete_table('network_candidate')


    models = {
        'annotations.animal': {
            'Meta': {'object_name': 'Animal'},
            'alternative_names': ('django.db.models.fields.CharField', [], {'max_length': '21', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'annotations.species': {
            'Meta': {'object_name': 'Species'},
            'alternative_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Animal']", 'symmetrical': 'False', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'complexity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gendr_genes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gendr_orthologs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gendr_paralogs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'latin_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'main_model': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_genes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_latin_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'media.image': {
            'Meta': {'object_name': 'Image'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'related_name': "'uploader'", 'to': "orm['auth.User']"})
        },
        'network.analysis': {
            'Meta': {'object_name': 'Analysis'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['annotations.Species']"}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'network.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'analysis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['network.Analysis']"}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['annotations.Species']", 'null': 'True', 'blank': 'True'}),
            'specificity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            't': ('django.db.models.fields.IntegerField', [], {}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'worm_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'worm_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'yeast_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'yeast_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'network.enrichment': {
            'Meta': {'object_name': 'Enrichment'},
            'analysis': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['network.Analysis']"}),
            'genes': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pvalue': ('django.db.models.fields.FloatField', [], {}),
            'r': ('django.db.models.fields.FloatField', [], {}),
            's': ('django.db.models.fields.IntegerField', [], {}),
            't': ('django.db.models.fields.IntegerField', [], {}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['network']