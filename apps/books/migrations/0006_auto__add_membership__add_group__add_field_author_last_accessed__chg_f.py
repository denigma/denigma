# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Membership'
        db.create_table('books_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Person'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Group'])),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
            ('invite_reason', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('books', ['Membership'])

        # Adding model 'Group'
        db.create_table('books_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('books', ['Group'])

        # Adding field 'Author.last_accessed'
        db.add_column('books_author', 'last_accessed', self.gf('django.db.models.fields.DateField')(default=None, blank=True), keep_default=False)

        # Changing field 'Person.birth_date'
        db.alter_column('books_person', 'birth_date', self.gf('django.db.models.fields.DateField')(null=True))


    def backwards(self, orm):
        
        # Deleting model 'Membership'
        db.delete_table('books_membership')

        # Deleting model 'Group'
        db.delete_table('books_group')

        # Deleting field 'Author.last_accessed'
        db.delete_column('books_author', 'last_accessed')

        # Changing field 'Person.birth_date'
        db.alter_column('books_person', 'birth_date', self.gf('django.db.models.fields.DateField')(default=None))


    models = {
        'books.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_accessed': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['books.Author']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_pages': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Publisher']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'books.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membrs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['books.Person']", 'through': "orm['books.Membership']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'books.membership': {
            'Meta': {'object_name': 'Membership'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_reason': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Person']"})
        },
        'books.person': {
            'Meta': {'object_name': 'Person'},
            'adress': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'birth_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'books.publisher': {
            'Meta': {'ordering': "['name']", 'object_name': 'Publisher'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'state_province': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['books']
