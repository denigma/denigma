# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Questionnaire'
        db.create_table('questionnaire_questionnaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('questionnaire', ['Questionnaire'])

        # Adding model 'Section'
        db.create_table('questionnaire_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sections', null=True, to=orm['questionnaire.Questionnaire'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('questionnaire', ['Section'])

        # Adding unique constraint on 'Section', fields ['questionnaire', 'order']
        db.create_unique('questionnaire_section', ['questionnaire_id', 'order'])

        # Adding model 'Question'
        db.create_table('questionnaire_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('choices', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('answer_type', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='questions', null=True, to=orm['questionnaire.Section'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('questionnaire', ['Question'])

        # Adding unique constraint on 'Question', fields ['section', 'order']
        db.create_unique('questionnaire_question', ['section_id', 'order'])

        # Adding model 'UserQuestionnaire'
        db.create_table('questionnaire_userquestionnaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='questionnaires', null=True, to=orm['auth.User'])),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='user_questionnaires', null=True, to=orm['questionnaire.Questionnaire'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('questionnaire', ['UserQuestionnaire'])

        # Adding model 'Answer'
        db.create_table('questionnaire_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(blank='True', related_name='answers', null=True, to=orm['questionnaire.Question'])),
            ('user_questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='answers', null=True, to=orm['questionnaire.UserQuestionnaire'])),
        ))
        db.send_create_signal('questionnaire', ['Answer'])


    def backwards(self, orm):
        # Removing unique constraint on 'Question', fields ['section', 'order']
        db.delete_unique('questionnaire_question', ['section_id', 'order'])

        # Removing unique constraint on 'Section', fields ['questionnaire', 'order']
        db.delete_unique('questionnaire_section', ['questionnaire_id', 'order'])

        # Deleting model 'Questionnaire'
        db.delete_table('questionnaire_questionnaire')

        # Deleting model 'Section'
        db.delete_table('questionnaire_section')

        # Deleting model 'Question'
        db.delete_table('questionnaire_question')

        # Deleting model 'UserQuestionnaire'
        db.delete_table('questionnaire_userquestionnaire')

        # Deleting model 'Answer'
        db.delete_table('questionnaire_answer')


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
        'questionnaire.answer': {
            'Meta': {'ordering': "['question__section__order', 'question__order']", 'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'blank': "'True'", 'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.Question']"}),
            'user_questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.UserQuestionnaire']"})
        },
        'questionnaire.question': {
            'Meta': {'ordering': "['order']", 'unique_together': "[['section', 'order']]", 'object_name': 'Question'},
            'answer_type': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'choices': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questions'", 'null': 'True', 'to': "orm['questionnaire.Section']"})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '60'})
        },
        'questionnaire.section': {
            'Meta': {'ordering': "['order']", 'unique_together': "[['questionnaire', 'order']]", 'object_name': 'Section'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sections'", 'null': 'True', 'to': "orm['questionnaire.Questionnaire']"})
        },
        'questionnaire.userquestionnaire': {
            'Meta': {'ordering': "['user', 'created']", 'object_name': 'UserQuestionnaire'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user_questionnaires'", 'null': 'True', 'to': "orm['questionnaire.Questionnaire']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questionnaires'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['questionnaire']