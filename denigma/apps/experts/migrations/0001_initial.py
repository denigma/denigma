# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Day'
        db.create_table('experts_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('experts', ['Day'])

        # Adding model 'BusinessHour'
        db.create_table('experts_businesshour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experts.Day'])),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('experts', ['BusinessHour'])

        # Adding model 'WorkingHour'
        db.create_table('experts_workinghour', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experts.Profile'])),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['experts.Day'])),
            ('from_time', self.gf('django.db.models.fields.TimeField')()),
            ('to_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('experts', ['WorkingHour'])

        # Adding model 'OpeningTime'
        db.create_table('experts_openingtime', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('experts', ['OpeningTime'])

        # Adding model 'Institute'
        db.create_table('experts_institute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('experts', ['Institute'])

        # Adding model 'Profile'
        db.create_table('experts_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='data', unique=True, null=True, to=orm['auth.User'])),
            ('user_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('gender', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=1, null=True, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=60, blank=True)),
            ('msn', self.gf('django.db.models.fields.EmailField')(max_length=60, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('affliation', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('work', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('experts', ['Profile'])

        # Adding M2M table for field business_hours on 'Profile'
        db.create_table('experts_profile_business_hours', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['experts.profile'], null=False)),
            ('businesshour', models.ForeignKey(orm['experts.businesshour'], null=False))
        ))
        db.create_unique('experts_profile_business_hours', ['profile_id', 'businesshour_id'])


    def backwards(self, orm):
        # Deleting model 'Day'
        db.delete_table('experts_day')

        # Deleting model 'BusinessHour'
        db.delete_table('experts_businesshour')

        # Deleting model 'WorkingHour'
        db.delete_table('experts_workinghour')

        # Deleting model 'OpeningTime'
        db.delete_table('experts_openingtime')

        # Deleting model 'Institute'
        db.delete_table('experts_institute')

        # Deleting model 'Profile'
        db.delete_table('experts_profile')

        # Removing M2M table for field business_hours on 'Profile'
        db.delete_table('experts_profile_business_hours')


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
        'experts.businesshour': {
            'Meta': {'object_name': 'BusinessHour'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experts.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'experts.day': {
            'Meta': {'object_name': 'Day'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'experts.institute': {
            'Meta': {'object_name': 'Institute'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'experts.openingtime': {
            'Meta': {'object_name': 'OpeningTime'},
            'day': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'experts.profile': {
            'Meta': {'object_name': 'Profile'},
            'affliation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'business_hours': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['experts.BusinessHour']", 'symmetrical': 'False', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '60', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'msn': ('django.db.models.fields.EmailField', [], {'max_length': '60', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'data'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'work': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'working_hours': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['experts.Day']", 'symmetrical': 'False', 'through': "orm['experts.WorkingHour']", 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'})
        },
        'experts.workinghour': {
            'Meta': {'object_name': 'WorkingHour'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experts.Day']"}),
            'from_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experts.Profile']"}),
            'to_time': ('django.db.models.fields.TimeField', [], {})
        }
    }

    complete_apps = ['experts']