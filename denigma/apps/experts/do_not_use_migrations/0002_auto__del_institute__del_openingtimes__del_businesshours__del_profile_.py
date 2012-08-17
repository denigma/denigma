# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Institute'
        db.delete_table('users_institute')

        # Deleting model 'OpeningTimes'
        db.delete_table('users_openingtimes')

        # Deleting model 'BusinessHours'
        db.delete_table('users_businesshours')

        # Deleting model 'Profile'
        db.delete_table('users_profile')

        # Removing M2M table for field business_hours on 'Profile'
        db.delete_table('users_profile_business_hours')

        # Deleting model 'Day'
        db.delete_table('users_day')

        # Deleting model 'WorkingHours'
        db.delete_table('users_workinghours')


    def backwards(self, orm):
        
        # Adding model 'Institute'
        db.create_table('users_institute', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal('users', ['Institute'])

        # Adding model 'OpeningTimes'
        db.create_table('users_openingtimes', (
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('day', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('users', ['OpeningTimes'])

        # Adding model 'BusinessHours'
        db.create_table('users_businesshours', (
            ('start', self.gf('django.db.models.fields.TimeField')()),
            ('end', self.gf('django.db.models.fields.TimeField')()),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Day'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('users', ['BusinessHours'])

        # Adding model 'Profile'
        db.create_table('users_profile', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('instituition_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('primary_email', self.gf('django.db.models.fields.EmailField')(max_length=60, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('user_name', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_code', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True, blank=True)),
        ))
        db.send_create_signal('users', ['Profile'])

        # Adding M2M table for field business_hours on 'Profile'
        db.create_table('users_profile_business_hours', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['users.profile'], null=False)),
            ('businesshours', models.ForeignKey(orm['users.businesshours'], null=False))
        ))
        db.create_unique('users_profile_business_hours', ['profile_id', 'businesshours_id'])

        # Adding model 'Day'
        db.create_table('users_day', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('users', ['Day'])

        # Adding model 'WorkingHours'
        db.create_table('users_workinghours', (
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Profile'])),
            ('day', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.Day'])),
            ('to_time', self.gf('django.db.models.fields.TimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('users', ['WorkingHours'])


    models = {
        
    }

    complete_apps = ['users']
