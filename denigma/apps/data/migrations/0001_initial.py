# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Entry'
        db.create_table('data_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['data.Entry'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'creator', null=True, to=orm['auth.User'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'publisher', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('data', ['Entry'])

        # Adding M2M table for field tagged on 'Entry'
        db.create_table('data_entry_tagged', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['data.entry'], null=False)),
            ('tag', models.ForeignKey(orm['data.tag'], null=False))
        ))
        db.create_unique('data_entry_tagged', ['entry_id', 'tag_id'])

        # Adding M2M table for field images on 'Entry'
        db.create_table('data_entry_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['data.entry'], null=False)),
            ('photourl', models.ForeignKey(orm['media.photourl'], null=False))
        ))
        db.create_unique('data_entry_images', ['entry_id', 'photourl_id'])

        # Adding model 'Change'
        db.create_table('data_change', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['data.Change'])),
            ('of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entry', to=orm['data.Entry'])),
            ('by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', to=orm['auth.User'])),
            ('at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('data', ['Change'])

        # Adding M2M table for field tagged on 'Change'
        db.create_table('data_change_tagged', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('change', models.ForeignKey(orm['data.change'], null=False)),
            ('tag', models.ForeignKey(orm['data.tag'], null=False))
        ))
        db.create_unique('data_change_tagged', ['change_id', 'tag_id'])

        # Adding M2M table for field images on 'Change'
        db.create_table('data_change_images', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('change', models.ForeignKey(orm['data.change'], null=False)),
            ('photourl', models.ForeignKey(orm['media.photourl'], null=False))
        ))
        db.create_unique('data_change_images', ['change_id', 'photourl_id'])

        # Adding model 'Tag'
        db.create_table('data_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('data', ['Tag'])

        # Adding M2M table for field synonyms on 'Tag'
        db.create_table('data_tag_synonyms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_tag', models.ForeignKey(orm['data.tag'], null=False)),
            ('to_tag', models.ForeignKey(orm['data.tag'], null=False))
        ))
        db.create_unique('data_tag_synonyms', ['from_tag_id', 'to_tag_id'])

        # Adding model 'Relation'
        db.create_table('data_relation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fr', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'source', to=orm['data.Entry'])),
            ('be', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'type', to=orm['data.Entry'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'target', to=orm['data.Entry'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'maker', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('data', ['Relation'])

        # Adding model 'Alteration'
        db.create_table('data_alteration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fr', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source_entry', to=orm['data.Entry'])),
            ('be', self.gf('django.db.models.fields.related.ForeignKey')(related_name='type_of', to=orm['data.Entry'])),
            ('to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='target_entry', to=orm['data.Entry'])),
            ('of', self.gf('django.db.models.fields.related.ForeignKey')(related_name='relationship', to=orm['data.Relation'])),
            ('by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person', to=orm['auth.User'])),
            ('at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('data', ['Alteration'])


    def backwards(self, orm):
        # Deleting model 'Entry'
        db.delete_table('data_entry')

        # Removing M2M table for field tagged on 'Entry'
        db.delete_table('data_entry_tagged')

        # Removing M2M table for field images on 'Entry'
        db.delete_table('data_entry_images')

        # Deleting model 'Change'
        db.delete_table('data_change')

        # Removing M2M table for field tagged on 'Change'
        db.delete_table('data_change_tagged')

        # Removing M2M table for field images on 'Change'
        db.delete_table('data_change_images')

        # Deleting model 'Tag'
        db.delete_table('data_tag')

        # Removing M2M table for field synonyms on 'Tag'
        db.delete_table('data_tag_synonyms')

        # Deleting model 'Relation'
        db.delete_table('data_relation')

        # Deleting model 'Alteration'
        db.delete_table('data_alteration')


    models = {
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
        'data.alteration': {
            'Meta': {'object_name': 'Alteration'},
            'at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'be': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'type_of'", 'to': "orm['data.Entry']"}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person'", 'to': "orm['auth.User']"}),
            'fr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source_entry'", 'to': "orm['data.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'relationship'", 'to': "orm['data.Relation']"}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'target_entry'", 'to': "orm['data.Entry']"})
        },
        'data.change': {
            'Meta': {'object_name': 'Change'},
            'at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.PhotoUrl']", 'symmetrical': 'False', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry'", 'to': "orm['data.Entry']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['data.Change']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'tagged': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Tag']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'data.entry': {
            'Meta': {'object_name': 'Entry'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.PhotoUrl']", 'symmetrical': 'False', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['data.Entry']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'publisher'", 'null': 'True', 'to': "orm['auth.User']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'tagged': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Tag']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['data.Change']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'data.relation': {
            'Meta': {'object_name': 'Relation'},
            'be': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'type'", 'to': "orm['data.Entry']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'maker'", 'null': 'True', 'to': "orm['auth.User']"}),
            'fr': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'source'", 'to': "orm['data.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'target'", 'to': "orm['data.Entry']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['data.Alteration']", 'symmetrical': 'False'})
        },
        'data.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'synonyms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'synonyms_rel_+'", 'blank': 'True', 'to': "orm['data.Tag']"})
        },
        'media.photourl': {
            'Meta': {'object_name': 'PhotoUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['data']