# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hierarchy'
        db.create_table('aspects_hierarchy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('symbol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Image'])),
            ('requirement', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aspects.HierarchyType'], blank=True)),
        ))
        db.send_create_signal('aspects', ['Hierarchy'])

        # Adding model 'HierarchyType'
        db.create_table('aspects_hierarchytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('symbol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Image'])),
            ('requirement', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('aspects', ['HierarchyType'])

        # Adding model 'Rank'
        db.create_table('aspects_rank', (
            ('hierarchy_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aspects.Hierarchy'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('aspects', ['Rank'])

        # Adding model 'Grade'
        db.create_table('aspects_grade', (
            ('hierarchy_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aspects.Hierarchy'], unique=True, primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aspects.Language'])),
        ))
        db.send_create_signal('aspects', ['Grade'])

        # Adding model 'Title'
        db.create_table('aspects_title', (
            ('hierarchy_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aspects.Hierarchy'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('aspects', ['Title'])

        # Adding model 'Language'
        db.create_table('aspects_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('symbol', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Image'])),
            ('requirement', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('aspects', ['Language'])

        # Adding model 'Role'
        db.create_table('aspects_role', (
            ('hierarchy_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aspects.Hierarchy'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('aspects', ['Role'])


    def backwards(self, orm):
        # Deleting model 'Hierarchy'
        db.delete_table('aspects_hierarchy')

        # Deleting model 'HierarchyType'
        db.delete_table('aspects_hierarchytype')

        # Deleting model 'Rank'
        db.delete_table('aspects_rank')

        # Deleting model 'Grade'
        db.delete_table('aspects_grade')

        # Deleting model 'Title'
        db.delete_table('aspects_title')

        # Deleting model 'Language'
        db.delete_table('aspects_language')

        # Deleting model 'Role'
        db.delete_table('aspects_role')


    models = {
        'aspects.grade': {
            'Meta': {'object_name': 'Grade', '_ormbases': ['aspects.Hierarchy']},
            'hierarchy_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['aspects.Hierarchy']", 'unique': 'True', 'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aspects.Language']"})
        },
        'aspects.hierarchy': {
            'Meta': {'object_name': 'Hierarchy'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'requirement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Image']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['aspects.HierarchyType']", 'blank': 'True'})
        },
        'aspects.hierarchytype': {
            'Meta': {'object_name': 'HierarchyType'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'requirement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Image']"})
        },
        'aspects.language': {
            'Meta': {'object_name': 'Language'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'requirement': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media.Image']"})
        },
        'aspects.rank': {
            'Meta': {'object_name': 'Rank', '_ormbases': ['aspects.Hierarchy']},
            'hierarchy_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['aspects.Hierarchy']", 'unique': 'True', 'primary_key': 'True'})
        },
        'aspects.role': {
            'Meta': {'object_name': 'Role', '_ormbases': ['aspects.Hierarchy']},
            'hierarchy_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['aspects.Hierarchy']", 'unique': 'True', 'primary_key': 'True'})
        },
        'aspects.title': {
            'Meta': {'object_name': 'Title', '_ormbases': ['aspects.Hierarchy']},
            'hierarchy_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['aspects.Hierarchy']", 'unique': 'True', 'primary_key': 'True'})
        },
        'media.photourl': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['aspects']