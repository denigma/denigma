# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Link.tags'
        db.add_column('links_link', 'tags', self.gf('tagging.fields.TagField')(default=''), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Link.tags'
        db.delete_column('links_link', 'tags')


    models = {
        'links.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'links.link': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Link'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['links.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'publication_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2042, 3, 15, 0, 0)'}),
            'publication_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['links']
