# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Profile.nation'
        db.add_column('experts_profile', 'nation',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['links.Country'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Profile.nation'
        db.delete_column('experts_profile', 'nation_id')


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
        'data.category': {
            'Meta': {'object_name': 'Category'},
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'category'", 'null': 'True', 'to': "orm['data.Entry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'synonyms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'synonyms_rel_+'", 'blank': 'True', 'to': "orm['data.Category']"})
        },
        'data.change': {
            'Meta': {'object_name': 'Change'},
            'at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user'", 'to': "orm['auth.User']"}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Category']", 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'initial': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'of': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry'", 'to': "orm['data.Entry']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['data.Change']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'tagged': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Tag']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'data.entry': {
            'Meta': {'object_name': 'Entry'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Category']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['data.Entry']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'publisher'", 'null': 'True', 'to': "orm['auth.User']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'tagged': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Tag']", 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updates': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['data.Change']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'data.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'synonyms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'synonyms_rel_+'", 'blank': 'True', 'to': "orm['data.Tag']"})
        },
        'datasets.reference': {
            'Meta': {'object_name': 'Reference'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'accession_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'alternate_journal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'article_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author_address': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'call_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'references'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['data.Entry']"}),
            'database_provider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'epub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'legal_note': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name_of_database': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nihmsid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'original_publication': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '23', 'blank': 'True'}),
            'pmcid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'reprint_edition': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'research_notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'reviewed_items': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'start_page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'translated_author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type_of_article': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'experts.businesshour': {
            'Meta': {'object_name': 'BusinessHour'},
            'day': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experts.Day']"}),
            'end': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.TimeField', [], {})
        },
        'experts.collaboration': {
            'Meta': {'object_name': 'Collaboration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'labs': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['links.Link']", 'symmetrical': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'collaborations'", 'symmetrical': 'False', 'to': "orm['experts.Profile']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Entry']"})
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
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'business_hours': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['experts.BusinessHour']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'collaboration': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '60', 'blank': 'True'}),
            'entries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['data.Entry']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'msn': ('django.db.models.fields.EmailField', [], {'max_length': '60', 'blank': 'True'}),
            'nation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['links.Country']", 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'publications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['datasets.Reference']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'data'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'user_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'work': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
        },
        'links.category': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'links.country': {
            'Meta': {'object_name': 'Country'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'links.link': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Link'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'links'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['data.Entry']"}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['links.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['experts.Profile']", 'null': 'True', 'blank': 'True'}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['links.Country']", 'null': 'True', 'blank': 'True'}),
            'creation': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'publication_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2042, 3, 15, 0, 0)'}),
            'publication_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200'}),
            'visibility': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'media.image': {
            'Meta': {'object_name': 'Image'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '2', 'related_name': "'uploader'", 'to': "orm['auth.User']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['experts']