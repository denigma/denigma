# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('links_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('links', ['Category'])

        # Adding model 'Link'
        db.create_table('links_link', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=None, max_length=150)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=2)),
            ('url', self.gf('django.db.models.fields.URLField')(default=None, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('visibility', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=100)),
            ('creation', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('publication_start', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('publication_end', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2042, 3, 15, 0, 0))),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
        ))
        db.send_create_signal('links', ['Link'])

        # Adding M2M table for field category on 'Link'
        db.create_table('links_link_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('link', models.ForeignKey(orm['links.link'], null=False)),
            ('category', models.ForeignKey(orm['links.category'], null=False))
        ))
        db.create_unique('links_link_category', ['link_id', 'category_id'])


    def backwards(self, orm):
        
        # Deleting model 'Category'
        db.delete_table('links_category')

        # Deleting model 'Link'
        db.delete_table('links_link')

        # Removing M2M table for field category on 'Link'
        db.delete_table('links_link_category')


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
