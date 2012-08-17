# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Gene.gene_symbol'
        db.add_column('annotations_gene', 'gene_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)

        # Adding field 'Gene.classes'
        db.add_column('annotations_gene', 'classes', self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Gene.gene_symbol'
        db.delete_column('annotations_gene', 'gene_symbol')

        # Deleting field 'Gene.classes'
        db.delete_column('annotations_gene', 'classes')


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
        'annotations.ensemblhomolog': {
            'Meta': {'object_name': 'EnsemblHomolog'},
            'dn': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ds': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ensembl_gene_id_a': ('django.db.models.fields.CharField', [], {'max_length': '18', 'db_index': 'True'}),
            'ensembl_gene_id_b': ('django.db.models.fields.CharField', [], {'max_length': '18', 'db_index': 'True'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity_a': ('django.db.models.fields.IntegerField', [], {}),
            'percentage_identity_b': ('django.db.models.fields.IntegerField', [], {}),
            'potential_homolog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'taxid_a': ('django.db.models.fields.IntegerField', [], {}),
            'taxid_b': ('django.db.models.fields.IntegerField', [], {})
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
        'annotations.orthologs_4932_10090': {
            'Meta': {'object_name': 'Orthologs_4932_10090'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mouse_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'mouse_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.orthologs_4932_10116': {
            'Meta': {'object_name': 'Orthologs_4932_10116'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'rat_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'rat_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.orthologs_4932_6239': {
            'Meta': {'object_name': 'Orthologs_4932_6239'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'elegans_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'elegans_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.orthologs_4932_7227': {
            'Meta': {'object_name': 'Orthologs_4932_7227'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'drosophila_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'drosophila_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.orthologs_4932_9544': {
            'Meta': {'object_name': 'Orthologs_4932_9544'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'rhesus_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'rhesus_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.orthologs_4932_9606': {
            'Meta': {'object_name': 'Orthologs_4932_9606'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'human_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'human_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.paralogs_4932_4932': {
            'Meta': {'object_name': 'Paralogs_4932_4932'},
            'bootstrap_duplication_confidence_score': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bootstrap_duplication_confidence_score_type': ('django.db.models.fields.CharField', [], {'max_length': '46', 'blank': 'True'}),
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '22', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'yeast_paralog_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'yeast_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.potentialorthologs_4932_10090': {
            'Meta': {'object_name': 'PotentialOrthologs_4932_10090'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mouse_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'mouse_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.potentialorthologs_4932_10116': {
            'Meta': {'object_name': 'PotentialOrthologs_4932_10116'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'rat_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'rat_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.potentialorthologs_4932_6239': {
            'Meta': {'object_name': 'PotentialOrthologs_4932_6239'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'elegans_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.potentialorthologs_4932_7227': {
            'Meta': {'object_name': 'PotentialOrthologs_4932_7227'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'drosophila_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'drosophila_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.potentialorthologs_4932_9544': {
            'Meta': {'object_name': 'PotentialOrthologs_4932_9544'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'rhesus_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'rhesus_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
        },
        'annotations.potentialorthologs_4932_9606': {
            'Meta': {'object_name': 'PotentialOrthologs_4932_9606'},
            'dn': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ds': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'homology_type': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'human_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'human_percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'percentage_identity': ('django.db.models.fields.IntegerField', [], {'blank': 'True'})
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
