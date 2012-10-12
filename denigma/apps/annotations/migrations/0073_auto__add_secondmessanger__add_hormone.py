# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SecondMessanger'
        db.create_table('annotations_secondmessanger', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('stimulator', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('annotations', ['SecondMessanger'])

        # Adding model 'Hormone'
        db.create_table('annotations_hormone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('symbol', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('effects', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('annotations', ['Hormone'])

        # Adding M2M table for field tissues on 'Hormone'
        db.create_table('annotations_hormone_tissues', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hormone', models.ForeignKey(orm['annotations.hormone'], null=False)),
            ('tissue', models.ForeignKey(orm['annotations.tissue'], null=False))
        ))
        db.create_unique('annotations_hormone_tissues', ['hormone_id', 'tissue_id'])


    def backwards(self, orm):
        # Deleting model 'SecondMessanger'
        db.delete_table('annotations_secondmessanger')

        # Deleting model 'Hormone'
        db.delete_table('annotations_hormone')

        # Removing M2M table for field tissues on 'Hormone'
        db.delete_table('annotations_hormone_tissues')


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
            'dr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
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
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'annotations.discontinuedid': {
            'Meta': {'object_name': 'DiscontinuedId'},
            'discontinued_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.ensemblentrezgeneid': {
            'Meta': {'object_name': 'EnsemblEntrezGeneId'},
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
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
        'annotations.entrez_gene': {
            'Meta': {'object_name': 'Entrez_Gene'},
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'full_name_from_nomenclature_autority': ('django.db.models.fields.CharField', [], {'max_length': '251', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'hgnc': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'hprd': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'imgt_gene_db': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'mgi': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'mim': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'mirbase': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'ratmap': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'rgd': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'symbol_from_nomenclature_authority': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        },
        'annotations.gen': {
            'Meta': {'object_name': 'Gen'},
            'ageing_associated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ageing_differential': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ageing_induced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ageing_methylated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ageing_suppressed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ageing_suppressor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'circadian_differential': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '33'}),
            'clock_modulator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clock_modulator_ortholog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clock_systemic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'core_clock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dr_differential': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dr_essential': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dr_essential_ortholog': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dr_induced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dr_suppressed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'embryonic_lethal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '173', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gerontogene': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'high_amplitude': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'imprinted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'juvenile_associated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'juvenile_differential': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'juvenile_induced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'juvenile_suppressed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'long_period': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'longevity_associated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'maternal_imprinted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'negative_ageing_suppressor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'negative_gerontogene': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pacemaker': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paternal_imprinted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'positive_ageing_suppressor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'positive_gerontogene': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'senescence_differential': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'senescence_induced': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'senescence_suppressed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_period': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {}),
            'transcription_factor': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'annotations.gene': {
            'Meta': {'object_name': 'Gene'},
            'classes': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'classification': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Classification']", 'symmetrical': 'False'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.gene2ensembl': {
            'Meta': {'object_name': 'gene2ensembl'},
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'db_index': 'True'}),
            'ensembl_protein_id': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'ensembl_rna_id': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein_accession': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'rna_nucleotide_accession': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'annotations.go': {
            'Meta': {'object_name': 'GO'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {}),
            'evidence': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'go_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'go_term': ('django.db.models.fields.CharField', [], {'max_length': '193'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pmid': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'qualifier': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
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
        'annotations.hormone': {
            'Meta': {'object_name': 'Hormone'},
            'effects': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tissues': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Tissue']", 'symmetrical': 'False'})
        },
        'annotations.inparanoid': {
            'Meta': {'object_name': 'InParanoid'},
            'ensembl_gene_id_a': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ensembl_gene_id_b': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'group_number': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taxid_a': ('django.db.models.fields.IntegerField', [], {}),
            'taxid_b': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.ortholog': {
            'Meta': {'object_name': 'Ortholog'},
            'gene': ('django.db.models.fields.IntegerField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'gene_taxid': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ortholog': ('django.db.models.fields.IntegerField', [], {}),
            'ortholog_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'ortholog_taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'annotations.secondmessanger': {
            'Meta': {'object_name': 'SecondMessanger'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stimulator': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
            'alternative_names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['annotations.Animal']", 'symmetrical': 'False', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'complexity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gendr_genes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gendr_orthologs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gendr_paralogs': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'latin_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'main_model': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_genes': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'short_latin_name': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        'annotations.taxonomy': {
            'Meta': {'object_name': 'Taxonomy', 'db_table': "u'taxonomy'"},
            'acronyms': ('django.db.models.fields.CharField', [], {'max_length': '147', 'blank': 'True'}),
            'adult_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'anamorphs': ('django.db.models.fields.CharField', [], {'max_length': '213', 'blank': 'True'}),
            'authorities': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'birth_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'blast_name': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'body_mass': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'classis': ('django.db.models.fields.CharField', [], {'max_length': '84', 'blank': 'True'}),
            'common_names': ('django.db.models.fields.CharField', [], {'max_length': '534', 'blank': 'True'}),
            'data_quality': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'equivalent_names': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'family': ('django.db.models.fields.CharField', [], {'max_length': '129', 'blank': 'True'}),
            'female_maturity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'forma': ('django.db.models.fields.CharField', [], {'max_length': '135', 'blank': 'True'}),
            'genbank_acronym': ('django.db.models.fields.CharField', [], {'max_length': '66', 'blank': 'True'}),
            'genbank_anamorph': ('django.db.models.fields.CharField', [], {'max_length': '117', 'blank': 'True'}),
            'genbank_common_name': ('django.db.models.fields.CharField', [], {'max_length': '171', 'blank': 'True'}),
            'genbank_synonym': ('django.db.models.fields.CharField', [], {'max_length': '168', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '147', 'blank': 'True'}),
            'gestation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'growth_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'imr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'in_parts': ('django.db.models.fields.CharField', [], {'max_length': '366', 'blank': 'True'}),
            'includes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'infraclass': ('django.db.models.fields.CharField', [], {'max_length': '42', 'blank': 'True'}),
            'infraorder': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'}),
            'inter_litters': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'kingdom': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'litter_rate': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'litters_size': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'male_maturity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maximum_longevity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'metabolic_rate': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'misnomers': ('django.db.models.fields.CharField', [], {'max_length': '687', 'blank': 'True'}),
            'misspellings': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'mrdt': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'no_rank': ('django.db.models.fields.CharField', [], {'max_length': '204', 'blank': 'True'}),
            'ordo': ('django.db.models.fields.CharField', [], {'max_length': '129', 'blank': 'True'}),
            'parvorder': ('django.db.models.fields.CharField', [], {'max_length': '42', 'blank': 'True'}),
            'phylum': ('django.db.models.fields.CharField', [], {'max_length': '102', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '531', 'blank': 'True'}),
            'sample_size': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '324', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '129', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '228', 'blank': 'True'}),
            'species_group': ('django.db.models.fields.CharField', [], {'max_length': '84', 'blank': 'True'}),
            'species_subgroup': ('django.db.models.fields.CharField', [], {'max_length': '84', 'blank': 'True'}),
            'specimen_origin': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'}),
            'subclass': ('django.db.models.fields.CharField', [], {'max_length': '93', 'blank': 'True'}),
            'subfamily': ('django.db.models.fields.CharField', [], {'max_length': '57', 'blank': 'True'}),
            'subgenus': ('django.db.models.fields.CharField', [], {'max_length': '93', 'blank': 'True'}),
            'subkingdom': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'suborder': ('django.db.models.fields.CharField', [], {'max_length': '93', 'blank': 'True'}),
            'subphylum': ('django.db.models.fields.CharField', [], {'max_length': '93', 'blank': 'True'}),
            'subspecies': ('django.db.models.fields.CharField', [], {'max_length': '111', 'blank': 'True'}),
            'subtribe': ('django.db.models.fields.CharField', [], {'max_length': '87', 'blank': 'True'}),
            'superclass': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'superfamily': ('django.db.models.fields.CharField', [], {'max_length': '84', 'blank': 'True'}),
            'superkingdom': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'}),
            'superorder': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'}),
            'superphylum': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'synonyms': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'teleomorph': ('django.db.models.fields.CharField', [], {'max_length': '117', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'tribe': ('django.db.models.fields.CharField', [], {'max_length': '87', 'blank': 'True'}),
            'unpublished_names': ('django.db.models.fields.CharField', [], {'max_length': '381', 'blank': 'True'}),
            'varietas': ('django.db.models.fields.CharField', [], {'max_length': '141', 'blank': 'True'}),
            'weaning_days': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weaning_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'annotations.tissue': {
            'Meta': {'object_name': 'Tissue'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'hierarchy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['media.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'synonyms': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'media.photourl': {
            'Meta': {'object_name': 'Image'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['annotations']