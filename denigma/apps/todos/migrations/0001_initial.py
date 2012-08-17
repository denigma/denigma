# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Todo'
        db.create_table('todos_todo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('importance', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('stop_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('todos', ['Todo'])


    def backwards(self, orm):
        
        # Deleting model 'Todo'
        db.delete_table('todos_todo')


    models = {
        'todos.todo': {
            'Meta': {'object_name': 'Todo'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['todos']
