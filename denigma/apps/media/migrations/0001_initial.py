# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

from media.migration_utils import was_applied


class Migration(SchemaMigration):

    def forwards(self, orm):

        if was_applied(__file__, 'gallery'):
            return

        # Adding model 'Image'
        db.create_table('gallery_photourl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('media', ['Image'])


    def backwards(self, orm):
        
        # Deleting model 'Image'
        db.delete_table('gallery_photourl')


    models = {
        'media.photourl': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['media']
