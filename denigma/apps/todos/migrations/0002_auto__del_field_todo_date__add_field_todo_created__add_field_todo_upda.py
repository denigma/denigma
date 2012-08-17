# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Todo.date'
        db.delete_column('todos_todo', 'date')

        # Adding field 'Todo.created'
        db.add_column('todos_todo', 'created', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=None, blank=True), keep_default=False)

        # Adding field 'Todo.updated'
        db.add_column('todos_todo', 'updated', self.gf('django.db.models.fields.DateField')(auto_now=True, default=None, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'Todo.date'
        raise RuntimeError("Cannot reverse this migration. 'Todo.date' and its values cannot be restored.")

        # Deleting field 'Todo.created'
        db.delete_column('todos_todo', 'created')

        # Deleting field 'Todo.updated'
        db.delete_column('todos_todo', 'updated')


    models = {
        'todos.todo': {
            'Meta': {'object_name': 'Todo'},
            'created': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importance': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stop_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['todos']
