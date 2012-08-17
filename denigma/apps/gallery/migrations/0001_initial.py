# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PhotoUrl'
        db.create_table('gallery_photourl', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('gallery', ['PhotoUrl'])


    def backwards(self, orm):
        
        # Deleting model 'PhotoUrl'
        db.delete_table('gallery_photourl')


    models = {
        'gallery.photourl': {
            'Meta': {'object_name': 'PhotoUrl'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['gallery']
