import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.contenttypes.models import ContentType


class Migration(DataMigration):

    def forwards(self):
        content_types = ContentType.objects.filter(app_label='gallery')
        content_types.update(app_label='media')

    def backwards(self, orm):
        content_types = ContentType.objects.filter(app_label='media')
        content_types.update(app_label='gallery')

    models = {
            'media.photourl': {
                'Meta': {'object_name': 'Image'},
                'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
                'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
                'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
            }
        }

complete_apps = ['media']