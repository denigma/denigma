# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Type'
        db.create_table('lifespan_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('lifespan', ['Type'])

        # Adding model 'Regimen'
        db.create_table('lifespan_regimen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('shortcut', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('lifespan', ['Regimen'])

        # Adding model 'Assay'
        db.create_table('lifespan_assay', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('shortcut', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('lifespan', ['Assay'])

        # Adding model 'Manipulation'
        db.create_table('lifespan_manipulation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shortcut', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('lifespan', ['Manipulation'])

        # Adding M2M table for field type on 'Manipulation'
        db.create_table('lifespan_manipulation_type', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_manipulation', models.ForeignKey(orm['lifespan.manipulation'], null=False)),
            ('to_manipulation', models.ForeignKey(orm['lifespan.manipulation'], null=False))
        ))
        db.create_unique('lifespan_manipulation_type', ['from_manipulation_id', 'to_manipulation_id'])

        # Adding model 'Intervention'
        db.create_table('lifespan_intervention', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('background', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('lifespans', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('effect', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('mean', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('median', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('_25', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('_75', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('maximum', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('pmid', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal('lifespan', ['Intervention'])

        # Adding M2M table for field references on 'Intervention'
        db.create_table('lifespan_intervention_references', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('intervention', models.ForeignKey(orm['lifespan.intervention'], null=False)),
            ('reference', models.ForeignKey(orm['datasets.reference'], null=False))
        ))
        db.create_unique('lifespan_intervention_references', ['intervention_id', 'reference_id'])

        # Adding M2M table for field manipulation on 'Intervention'
        db.create_table('lifespan_intervention_manipulation', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('intervention', models.ForeignKey(orm['lifespan.intervention'], null=False)),
            ('manipulation', models.ForeignKey(orm['lifespan.manipulation'], null=False))
        ))
        db.create_unique('lifespan_intervention_manipulation', ['intervention_id', 'manipulation_id'])

        # Adding model 'Factor'
        db.create_table('lifespan_factor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=244, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=270, blank=True)),
            ('function', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('functional_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('observation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('diet_regimen', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('life_span', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('pubmed_id', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('mean', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('median', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('maximum', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('_75', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('_25', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('manipulation', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('gene_intervention', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('synergistic_epistasis', self.gf('django.db.models.fields.CharField')(max_length=33, blank=True)),
            ('antagonistic_epistasis', self.gf('django.db.models.fields.CharField')(max_length=216, blank=True)),
            ('human_homologue', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
        ))
        db.send_create_signal('lifespan', ['Factor'])

        # Adding M2M table for field classifications on 'Factor'
        db.create_table('lifespan_factor_classifications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factor', models.ForeignKey(orm['lifespan.factor'], null=False)),
            ('classification', models.ForeignKey(orm['annotations.classification'], null=False))
        ))
        db.create_unique('lifespan_factor_classifications', ['factor_id', 'classification_id'])

        # Adding M2M table for field regimen on 'Factor'
        db.create_table('lifespan_factor_regimen', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factor', models.ForeignKey(orm['lifespan.factor'], null=False)),
            ('regimen', models.ForeignKey(orm['lifespan.regimen'], null=False))
        ))
        db.create_unique('lifespan_factor_regimen', ['factor_id', 'regimen_id'])

        # Adding M2M table for field assay on 'Factor'
        db.create_table('lifespan_factor_assay', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factor', models.ForeignKey(orm['lifespan.factor'], null=False)),
            ('assay', models.ForeignKey(orm['lifespan.assay'], null=False))
        ))
        db.create_unique('lifespan_factor_assay', ['factor_id', 'assay_id'])

        # Adding M2M table for field references on 'Factor'
        db.create_table('lifespan_factor_references', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factor', models.ForeignKey(orm['lifespan.factor'], null=False)),
            ('reference', models.ForeignKey(orm['datasets.reference'], null=False))
        ))
        db.create_unique('lifespan_factor_references', ['factor_id', 'reference_id'])

        # Adding M2M table for field intervention on 'Factor'
        db.create_table('lifespan_factor_intervention', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factor', models.ForeignKey(orm['lifespan.factor'], null=False)),
            ('intervention', models.ForeignKey(orm['lifespan.intervention'], null=False))
        ))
        db.create_unique('lifespan_factor_intervention', ['factor_id', 'intervention_id'])

        # Adding M2M table for field types on 'Factor'
        db.create_table('lifespan_factor_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('factor', models.ForeignKey(orm['lifespan.factor'], null=False)),
            ('type', models.ForeignKey(orm['lifespan.type'], null=False))
        ))
        db.create_unique('lifespan_factor_types', ['factor_id', 'type_id'])


    def backwards(self, orm):
        # Deleting model 'Type'
        db.delete_table('lifespan_type')

        # Deleting model 'Regimen'
        db.delete_table('lifespan_regimen')

        # Deleting model 'Assay'
        db.delete_table('lifespan_assay')

        # Deleting model 'Manipulation'
        db.delete_table('lifespan_manipulation')

        # Removing M2M table for field type on 'Manipulation'
        db.delete_table('lifespan_manipulation_type')

        # Deleting model 'Intervention'
        db.delete_table('lifespan_intervention')

        # Removing M2M table for field references on 'Intervention'
        db.delete_table('lifespan_intervention_references')

        # Removing M2M table for field manipulation on 'Intervention'
        db.delete_table('lifespan_intervention_manipulation')

        # Deleting model 'Factor'
        db.delete_table('lifespan_factor')

        # Removing M2M table for field classifications on 'Factor'
        db.delete_table('lifespan_factor_classifications')

        # Removing M2M table for field regimen on 'Factor'
        db.delete_table('lifespan_factor_regimen')

        # Removing M2M table for field assay on 'Factor'
        db.delete_table('lifespan_factor_assay')

        # Removing M2M table for field references on 'Factor'
        db.delete_table('lifespan_factor_references')

        # Removing M2M table for field intervention on 'Factor'
        db.delete_table('lifespan_factor_intervention')

        # Removing M2M table for field types on 'Factor'
        db.delete_table('lifespan_factor_types')


    models = {
        'annotations.classification': {
            'Meta': {'object_name': 'Classification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'datasets.reference': {
            'Meta': {'object_name': 'Reference', 'db_table': "u'reference'"},
            'access_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'accession_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'alternate_journal': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'article_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'author_address': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'authors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'call_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'database_provider': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'epub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'issue': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'journal': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'legal_note': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name_of_database': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'nihmsid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'original_publication': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'pages': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'pmcid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reprint_editione': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'research_notes': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reviewed_itemse': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'start_page': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'translated_author': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'type_of_article': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'lifespan.assay': {
            'Meta': {'object_name': 'Assay'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'lifespan.factor': {
            'Meta': {'object_name': 'Factor'},
            '_25': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            '_75': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '270', 'blank': 'True'}),
            'antagonistic_epistasis': ('django.db.models.fields.CharField', [], {'max_length': '216', 'blank': 'True'}),
            'assay': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifespan.Assay']", 'symmetrical': 'False'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'classifications': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Classification']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'diet_regimen': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'functional_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_intervention': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'human_homologue': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervention': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifespan.Intervention']", 'symmetrical': 'False', 'blank': 'True'}),
            'life_span': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'manipulation': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maximum': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mean': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'median': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '244', 'blank': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datasets.Reference']", 'symmetrical': 'False', 'blank': 'True'}),
            'regimen': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifespan.Regimen']", 'symmetrical': 'False', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'synergistic_epistasis': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifespan.Type']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'lifespan.intervention': {
            'Meta': {'object_name': 'Intervention'},
            '_25': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            '_75': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'background': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'effect': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifespans': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'manipulation': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lifespan.Manipulation']", 'symmetrical': 'False', 'blank': 'True'}),
            'maximum': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'mean': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'median': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'pmid': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'references': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datasets.Reference']", 'symmetrical': 'False', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'lifespan.manipulation': {
            'Meta': {'object_name': 'Manipulation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'type_of'", 'blank': 'True', 'to': "orm['lifespan.Manipulation']"})
        },
        'lifespan.regimen': {
            'Meta': {'object_name': 'Regimen'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'lifespan.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['lifespan']