# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'PotentialOrthologs_4932_10090'
        db.delete_table('annotations_potentialorthologs_4932_10090')

        # Deleting model 'Orthologs_4932_6239'
        db.delete_table('annotations_orthologs_4932_6239')

        # Deleting model 'PotentialOrthologs_4932_6239'
        db.delete_table('annotations_potentialorthologs_4932_6239')

        # Deleting model 'Orthologs_4932_7227'
        db.delete_table('annotations_orthologs_4932_7227')

        # Deleting model 'PotentialOrthologs_4932_7227'
        db.delete_table('annotations_potentialorthologs_4932_7227')

        # Deleting model 'Paralogs_4932_4932'
        db.delete_table('annotations_paralogs_4932_4932')

        # Deleting model 'PotentialOrthologs_4932_9544'
        db.delete_table('annotations_potentialorthologs_4932_9544')

        # Deleting model 'PotentialOrthologs_4932_9606'
        db.delete_table('annotations_potentialorthologs_4932_9606')

        # Deleting model 'EnsemblHomolog'
        db.delete_table('annotations_ensemblhomolog')

        # Deleting model 'Orthologs_4932_10090'
        db.delete_table('annotations_orthologs_4932_10090')

        # Deleting model 'PotentialOrthologs_4932_10116'
        db.delete_table('annotations_potentialorthologs_4932_10116')

        # Deleting model 'Orthologs_4932_9606'
        db.delete_table('annotations_orthologs_4932_9606')

        # Deleting model 'Orthologs_4932_9544'
        db.delete_table('annotations_orthologs_4932_9544')

        # Deleting model 'Orthologs_4932_10116'
        db.delete_table('annotations_orthologs_4932_10116')


    def backwards(self, orm):
        
        # Adding model 'PotentialOrthologs_4932_10090'
        db.create_table('annotations_potentialorthologs_4932_10090', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('mouse_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mouse_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['PotentialOrthologs_4932_10090'])

        # Adding model 'Orthologs_4932_6239'
        db.create_table('annotations_orthologs_4932_6239', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('elegans_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('elegans_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['Orthologs_4932_6239'])

        # Adding model 'PotentialOrthologs_4932_6239'
        db.create_table('annotations_potentialorthologs_4932_6239', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('elegans_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['PotentialOrthologs_4932_6239'])

        # Adding model 'Orthologs_4932_7227'
        db.create_table('annotations_orthologs_4932_7227', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('drosophila_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('drosophila_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['Orthologs_4932_7227'])

        # Adding model 'PotentialOrthologs_4932_7227'
        db.create_table('annotations_potentialorthologs_4932_7227', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('drosophila_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('drosophila_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['PotentialOrthologs_4932_7227'])

        # Adding model 'Paralogs_4932_4932'
        db.create_table('annotations_paralogs_4932_4932', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('yeast_paralog_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('bootstrap_duplication_confidence_score', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('yeast_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('bootstrap_duplication_confidence_score_type', self.gf('django.db.models.fields.CharField')(max_length=46, blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=22, blank=True)),
        ))
        db.send_create_signal('annotations', ['Paralogs_4932_4932'])

        # Adding model 'PotentialOrthologs_4932_9544'
        db.create_table('annotations_potentialorthologs_4932_9544', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('rhesus_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('rhesus_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['PotentialOrthologs_4932_9544'])

        # Adding model 'PotentialOrthologs_4932_9606'
        db.create_table('annotations_potentialorthologs_4932_9606', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('human_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('human_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['PotentialOrthologs_4932_9606'])

        # Adding model 'EnsemblHomolog'
        db.create_table('annotations_ensemblhomolog', (
            ('dn', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('taxid_b', self.gf('django.db.models.fields.IntegerField')()),
            ('taxid_a', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity_a', self.gf('django.db.models.fields.IntegerField')()),
            ('percentage_identity_b', self.gf('django.db.models.fields.IntegerField')()),
            ('ensembl_gene_id_a', self.gf('django.db.models.fields.CharField')(max_length=18, db_index=True)),
            ('ensembl_gene_id_b', self.gf('django.db.models.fields.CharField')(max_length=18, db_index=True)),
            ('potential_homolog', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
        ))
        db.send_create_signal('annotations', ['EnsemblHomolog'])

        # Adding model 'Orthologs_4932_10090'
        db.create_table('annotations_orthologs_4932_10090', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('mouse_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mouse_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['Orthologs_4932_10090'])

        # Adding model 'PotentialOrthologs_4932_10116'
        db.create_table('annotations_potentialorthologs_4932_10116', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('rat_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('rat_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['PotentialOrthologs_4932_10116'])

        # Adding model 'Orthologs_4932_9606'
        db.create_table('annotations_orthologs_4932_9606', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('human_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('human_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['Orthologs_4932_9606'])

        # Adding model 'Orthologs_4932_9544'
        db.create_table('annotations_orthologs_4932_9544', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('rhesus_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('rhesus_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['Orthologs_4932_9544'])

        # Adding model 'Orthologs_4932_10116'
        db.create_table('annotations_orthologs_4932_10116', (
            ('dn', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('homology_type', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('rat_ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('rat_percentage_identity', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('ds', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
        ))
        db.send_create_signal('annotations', ['Orthologs_4932_10116'])


    models = {
        'annotations.animal': {
            'Meta': {'object_name': 'Animal'},
            'alternative_names': ('django.db.models.fields.CharField', [], {'max_length': '21', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'annotations.candidate': {
            'Meta': {'object_name': 'Candidate', 'db_table': "u'Candidate'"},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'fly_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'fly_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'human_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'human_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mouse_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'mouse_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'p_value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_column': "'p-Value'", 'blank': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rat_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'rat_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            's': ('django.db.models.fields.IntegerField', [], {}),
            'seed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specificity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            't': ('django.db.models.fields.IntegerField', [], {}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'worm_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'worm_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'yeast_homolog_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'}),
            'yeast_homolog_symbol': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500', 'blank': 'True'})
        },
        'annotations.classification': {
            'Meta': {'object_name': 'Classification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        'annotations.discontinuedid': {
            'Meta': {'object_name': 'DiscontinuedId'},
            'discontinued_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.entrez': {
            'Meta': {'object_name': 'Entrez'},
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'full_name_from_nomenclature_autority': ('django.db.models.fields.CharField', [], {'max_length': '251', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'hgnc': ('django.db.models.fields.IntegerField', [], {}),
            'hprd': ('django.db.models.fields.IntegerField', [], {}),
            'imgt_gene_db': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'mgi': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'mim': ('django.db.models.fields.IntegerField', [], {}),
            'mirbase': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'ratmap': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'rgd': ('django.db.models.fields.IntegerField', [], {}),
            'symbol_from_nomeclature_authority': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        },
        'annotations.gene': {
            'Meta': {'object_name': 'Gene'},
            'classes': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'classification': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Classification']", 'symmetrical': 'False'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.go': {
            'Meta': {'object_name': 'GO'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'go_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'go_term': ('django.db.models.fields.CharField', [], {'max_length': '193'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pmid': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'qualifier': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.homologene': {
            'Meta': {'object_name': 'HomoloGene'},
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'hid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein_accession': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'protein_gi': ('django.db.models.fields.IntegerField', [], {}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.sgd_features': {
            'Meta': {'object_name': 'SGD_features'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'chromosome': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'coordinate_version': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'feature_qualifier': ('django.db.models.fields.CharField', [], {'max_length': '22', 'blank': 'True'}),
            'feature_type': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'genetic_position': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_feature_name': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'secondary_sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'}),
            'sequence_version': ('django.db.models.fields.CharField', [], {'max_length': '43'}),
            'sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'start_coordinate': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'stop_coordinate': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'strand': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        'annotations.sgd_gene_association': {
            'Meta': {'object_name': 'SGD_gene_association'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'date': ('django.db.models.fields.IntegerField', [], {}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '72'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'go_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '54'}),
            'other_ids': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'with_or_from': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        'annotations.species': {
            'Meta': {'object_name': 'Species'},
            'alternative_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Animal']", 'symmetrical': 'False'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'latin_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'latin_shortcut': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'number_genes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['annotations']
