# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Group.facebook_page__id'
        db.delete_column('southtut_group', 'facebook_page__id')

        # Adding field 'Group.facebook_page_id'
        db.add_column('southtut_group', 'facebook_page_id', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Changing field 'Group.name'
        db.alter_column('southtut_group', 'name', self.gf('django.db.models.fields.CharField')(max_length=255))


    def backwards(self, orm):
        
        # Adding field 'Group.facebook_page__id'
        db.add_column('southtut_group', 'facebook_page__id', self.gf('django.db.models.fields.CharField')(default='', max_length=255), keep_default=False)

        # Deleting field 'Group.facebook_page_id'
        db.delete_column('southtut_group', 'facebook_page_id')

        # Changing field 'Group.name'
        db.alter_column('southtut_group', 'name', self.gf('django.db.models.fields.TextField')())


    models = {
        'southtut.group': {
            'Meta': {'object_name': 'Group'},
            'facebook_page_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'southtut.knight': {
            'Meta': {'object_name': 'Knight'},
            'dances_whenever_able': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'of_the_round_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shrubberies': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['southtut']
