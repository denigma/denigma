# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('wiki_tag', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
        ))
        db.send_create_signal('wiki', ['Tag'])

        # Adding M2M table for field tags on 'Page'
        db.create_table('wiki_page_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('page', models.ForeignKey(orm['wiki.page'], null=False)),
            ('tag', models.ForeignKey(orm['wiki.tag'], null=False))
        ))
        db.create_unique('wiki_page_tags', ['page_id', 'tag_id'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('wiki_tag')

        # Removing M2M table for field tags on 'Page'
        db.delete_table('wiki_page_tags')


    models = {
        'wiki.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['wiki.Tag']", 'symmetrical': 'False'})
        },
        'wiki.tag': {
            'Meta': {'object_name': 'Tag'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        }
    }

    complete_apps = ['wiki']
