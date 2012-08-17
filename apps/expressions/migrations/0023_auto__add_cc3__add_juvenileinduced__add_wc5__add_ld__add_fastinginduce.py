# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Cc3'
        db.create_table('expressions_cc3', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_id_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fourier_f24', self.gf('django.db.models.fields.FloatField')()),
            ('fourier_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('anova_cc_f', self.gf('django.db.models.fields.FloatField')()),
            ('anova_cc_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('phase', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_avg', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_max', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_cc', self.gf('django.db.models.fields.FloatField')()),
            ('expression_avg', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ws195_wormbase_goterm_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('cycling', self.gf('django.db.models.fields.CharField')(max_length=54)),
        ))
        db.send_create_signal('expressions', ['Cc3'])

        # Adding model 'JuvenileInduced'
        db.create_table('expressions_juvenileinduced', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('probe_set', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=94)),
            ('heart', self.gf('django.db.models.fields.FloatField')()),
            ('kidney', self.gf('django.db.models.fields.FloatField')()),
            ('lung', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('expressions', ['JuvenileInduced'])

        # Adding model 'Wc5'
        db.create_table('expressions_wc5', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_id_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fourier_f24', self.gf('django.db.models.fields.FloatField')()),
            ('fourier_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('anova_f', self.gf('django.db.models.fields.FloatField')()),
            ('anova_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('phase', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_avg', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_max', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_wc', self.gf('django.db.models.fields.FloatField')()),
            ('expression_avg', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('ws195_wormbase_goterm_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('cycling', self.gf('django.db.models.fields.CharField')(max_length=54)),
        ))
        db.send_create_signal('expressions', ['Wc5'])

        # Adding model 'Ld'
        db.create_table('expressions_ld', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('anova_f_stat', self.gf('django.db.models.fields.FloatField')()),
            ('anova_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('ct_number', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('genbank_accession_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('expressions', ['Ld'])

        # Adding model 'FastingInducedGenes'
        db.create_table('expressions_fastinginducedgenes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('ncbi_kogs', self.gf('django.db.models.fields.CharField')(max_length=66, blank=True)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('expressions', ['FastingInducedGenes'])

        # Adding model 'Wccc6'
        db.create_table('expressions_wccc6', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_id_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fourier_f24', self.gf('django.db.models.fields.FloatField')()),
            ('fourier_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('anova_cc_f', self.gf('django.db.models.fields.FloatField')()),
            ('anova_cc_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('phase', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_avg', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_max', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_wc', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_cc', self.gf('django.db.models.fields.FloatField')()),
            ('expression_avg', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ws195_wormbase_goterm_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('cycling', self.gf('django.db.models.fields.CharField')(max_length=52)),
        ))
        db.send_create_signal('expressions', ['Wccc6'])

        # Adding model 'AgingTranscriptome'
        db.create_table('expressions_agingtranscriptome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('unigene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=162)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('chromosome', self.gf('django.db.models.fields.IntegerField')()),
            ('rna_nucleotide_accession_version', self.gf('django.db.models.fields.CharField')(max_length=219, blank=True)),
            ('changes_in_aging', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('expressions', ['AgingTranscriptome'])

        # Adding model 'CrTranscriptome'
        db.create_table('expressions_crtranscriptome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('unigene_id', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('chromosome', self.gf('django.db.models.fields.IntegerField')()),
            ('rna_nucleotide_accession_version', self.gf('django.db.models.fields.CharField')(max_length=155, blank=True)),
            ('changes_in_cr', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('expressions', ['CrTranscriptome'])

        # Adding model 'CrSignature'
        db.create_table('expressions_crsignature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=99)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('overexp', self.gf('django.db.models.fields.IntegerField')()),
            ('underexp', self.gf('django.db.models.fields.IntegerField')()),
            ('p_value', self.gf('django.db.models.fields.FloatField')()),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('expressions', ['CrSignature'])

        # Adding model 'Dd'
        db.create_table('expressions_dd', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('anova_f_stat', self.gf('django.db.models.fields.FloatField')()),
            ('anova_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('ct_number', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('genbank_accession_number', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('expressions', ['Dd'])

        # Adding model 'Lddd6'
        db.create_table('expressions_lddd6', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_id_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fourier_f24', self.gf('django.db.models.fields.FloatField')()),
            ('fourier_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('anova_dd_f', self.gf('django.db.models.fields.FloatField')()),
            ('anova_dd_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('phase', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_avg', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_max', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_ld', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_dd', self.gf('django.db.models.fields.FloatField')()),
            ('expression_avg', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ws195_wormbase_goterm_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('cycling', self.gf('django.db.models.fields.CharField')(max_length=52)),
        ))
        db.send_create_signal('expressions', ['Lddd6'])

        # Adding model 'AgingLui2010'
        db.create_table('expressions_aginglui2010', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('observation', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('pubmedid', self.gf('django.db.models.fields.IntegerField')()),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('expressions', ['AgingLui2010'])

        # Adding model 'Ld3'
        db.create_table('expressions_ld3', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_id_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fourier_f24', self.gf('django.db.models.fields.FloatField')()),
            ('fourier_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('anova_f', self.gf('django.db.models.fields.FloatField')()),
            ('anova_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('phase', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_avg', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_max', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_ld', self.gf('django.db.models.fields.FloatField')()),
            ('expression_avg', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('ws195_wormbase_goterm_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('cycling', self.gf('django.db.models.fields.CharField')(max_length=54)),
        ))
        db.send_create_signal('expressions', ['Ld3'])

        # Adding model 'Dd3'
        db.create_table('expressions_dd3', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('affymetrix_probe_id_set', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('fourier_f24', self.gf('django.db.models.fields.FloatField')()),
            ('fourier_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('anova_f', self.gf('django.db.models.fields.FloatField')()),
            ('anova_pvalue', self.gf('django.db.models.fields.FloatField')()),
            ('phase', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_avg', self.gf('django.db.models.fields.FloatField')()),
            ('ac24_max', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_dd', self.gf('django.db.models.fields.FloatField')()),
            ('expression_avg', self.gf('django.db.models.fields.FloatField')()),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('locus_tag', self.gf('django.db.models.fields.CharField')(max_length=11)),
            ('ws195_wormbase_gene_goterm_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wormbase_id', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('cycling', self.gf('django.db.models.fields.CharField')(max_length=54)),
        ))
        db.send_create_signal('expressions', ['Dd3'])

        # Adding model 'Swindell2009'
        db.create_table('expressions_swindell2009', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('observation', self.gf('django.db.models.fields.CharField')(max_length=172, blank=True)),
            ('pubmed_id', self.gf('django.db.models.fields.IntegerField')()),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=14, blank=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('p_value', self.gf('django.db.models.fields.FloatField')()),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
        ))
        db.send_create_signal('expressions', ['Swindell2009'])

        # Adding model 'ImprintedGeneNetwork'
        db.create_table('expressions_imprintedgenenetwork', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('lung_fold_change_1_to_4wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lung_p_value_1_to_4wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lung_fold_change_1_to_8wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lung_p_value_1_to_8wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('kidney_fold_change_1_to_4wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('kidney_p_value_1_to_4wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('kidney_fold_change_1_to_8wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('kidney_p_value_1_to_8wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('heart_fold_change_1_to_4wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('heart_p_value_1_to_4wk', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('consistency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('p_value', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('fold_change_higher_as_5', self.gf('django.db.models.fields.CharField')(max_length=3, blank=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal('expressions', ['ImprintedGeneNetwork'])

        # Adding model 'PostnatalGeneticProgram'
        db.create_table(u'postnatal_genetic_program', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('fold_change_from_1_to_4_wk_mouse_heart', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_4_wk_mouse_heart', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_from_1_to_4_wk_mouse_kidney', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_4_wk_mouse_kidney', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_from_1_to_8_wk_mouse_kidney', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_8_wk_mouse_kidney', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_from_1_to_4_wk_mouse_lung', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_4_wk_mouse_lung', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_from_1_to_8_wk_mouse_lung', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_8_wk_mouse_lung', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_from_1_to_5_wk_rat_lung', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_5_wk_rat_lung', self.gf('django.db.models.fields.FloatField')()),
            ('fold_change_from_1_to_5_wk_rat_kidney', self.gf('django.db.models.fields.FloatField')()),
            ('p_value_1_vs_5_wk_rat_kidney', self.gf('django.db.models.fields.FloatField')()),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('expressions', ['PostnatalGeneticProgram'])

        # Adding model 'Cd'
        db.create_table('expressions_cd', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('scn', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('liv', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('kid', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('aor', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('skm', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('hat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('adg', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('bat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('wat', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('bon', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pfr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('wb', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('atr', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ven', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('num_tissue', self.gf('django.db.models.fields.IntegerField')()),
            ('range_p', self.gf('django.db.models.fields.FloatField')()),
            ('peak_mean', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('expressions', ['Cd'])

        # Adding model 'JuvenileSuppressed'
        db.create_table(u'finkelstein2009_js', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('probe_set', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=99)),
            ('heart', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('kidney', self.gf('django.db.models.fields.FloatField')()),
            ('lung', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('expressions', ['JuvenileSuppressed'])


    def backwards(self, orm):
        
        # Deleting model 'Cc3'
        db.delete_table('expressions_cc3')

        # Deleting model 'JuvenileInduced'
        db.delete_table('expressions_juvenileinduced')

        # Deleting model 'Wc5'
        db.delete_table('expressions_wc5')

        # Deleting model 'Ld'
        db.delete_table('expressions_ld')

        # Deleting model 'FastingInducedGenes'
        db.delete_table('expressions_fastinginducedgenes')

        # Deleting model 'Wccc6'
        db.delete_table('expressions_wccc6')

        # Deleting model 'AgingTranscriptome'
        db.delete_table('expressions_agingtranscriptome')

        # Deleting model 'CrTranscriptome'
        db.delete_table('expressions_crtranscriptome')

        # Deleting model 'CrSignature'
        db.delete_table('expressions_crsignature')

        # Deleting model 'Dd'
        db.delete_table('expressions_dd')

        # Deleting model 'Lddd6'
        db.delete_table('expressions_lddd6')

        # Deleting model 'AgingLui2010'
        db.delete_table('expressions_aginglui2010')

        # Deleting model 'Ld3'
        db.delete_table('expressions_ld3')

        # Deleting model 'Dd3'
        db.delete_table('expressions_dd3')

        # Deleting model 'Swindell2009'
        db.delete_table('expressions_swindell2009')

        # Deleting model 'ImprintedGeneNetwork'
        db.delete_table('expressions_imprintedgenenetwork')

        # Deleting model 'PostnatalGeneticProgram'
        db.delete_table(u'postnatal_genetic_program')

        # Deleting model 'Cd'
        db.delete_table('expressions_cd')

        # Deleting model 'JuvenileSuppressed'
        db.delete_table(u'finkelstein2009_js')


    models = {
        'expressions.agemap': {
            'Meta': {'object_name': 'AgeMap'},
            'adrenals_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'cerebellum_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'empirical_meta_analysis_p_value': ('django.db.models.fields.FloatField', [], {}),
            'empirical_meta_analysis_value': ('django.db.models.fields.FloatField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'eye_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'gene_ontology': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'gonads_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'heart_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lung_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'spinal_cord_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'spleen_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'thymus_age_coef': ('django.db.models.fields.FloatField', [], {}),
            'unigene': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'expressions.aginglui2010': {
            'Meta': {'object_name': 'AgingLui2010'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.CharField', [], {'max_length': '95'}),
            'pubmedid': ('django.db.models.fields.IntegerField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'expressions.agingsignature': {
            'Meta': {'object_name': 'AgingSignature'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '93', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'human_brain': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'human_kidney': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'human_muscle_1': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'human_muscle_2': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mouse_brain': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_cochlea': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_eye': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_heart': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_hematopoietic': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_hippocampus': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_kidney': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_liver': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_lung': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_muscle': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_myoblast': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'mouse_neocortex': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'n_genes': ('django.db.models.fields.IntegerField', [], {}),
            'n_overexpressed': ('django.db.models.fields.IntegerField', [], {}),
            'n_underexpressed': ('django.db.models.fields.IntegerField', [], {}),
            'p_value': ('django.db.models.fields.FloatField', [], {}),
            'q_value': ('django.db.models.fields.FloatField', [], {}),
            'rat_cardiac': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_extraocular': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_glia': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_hippocampal_ca1_1': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_hippocampal_ca1_2': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_hippocampus': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_larynge': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_muscle': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_oculomotor': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_spinal': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'rat_stromal': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'expressions.agingsignaturechi': {
            'Meta': {'object_name': 'AgingSignatureChi'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '89', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'human_brain': ('django.db.models.fields.FloatField', [], {}),
            'human_kidney': ('django.db.models.fields.FloatField', [], {}),
            'human_muscle_1': ('django.db.models.fields.FloatField', [], {}),
            'human_muscle_2': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mouse_brain': ('django.db.models.fields.FloatField', [], {}),
            'mouse_cochlea': ('django.db.models.fields.FloatField', [], {}),
            'mouse_eye': ('django.db.models.fields.FloatField', [], {}),
            'mouse_heart': ('django.db.models.fields.FloatField', [], {}),
            'mouse_hematopoietic': ('django.db.models.fields.FloatField', [], {}),
            'mouse_hippocampus': ('django.db.models.fields.FloatField', [], {}),
            'mouse_kidney': ('django.db.models.fields.FloatField', [], {}),
            'mouse_liver': ('django.db.models.fields.FloatField', [], {}),
            'mouse_lung': ('django.db.models.fields.FloatField', [], {}),
            'mouse_muscle': ('django.db.models.fields.FloatField', [], {}),
            'mouse_myoblast': ('django.db.models.fields.FloatField', [], {}),
            'mouse_neocortex': ('django.db.models.fields.FloatField', [], {}),
            'n_genes': ('django.db.models.fields.IntegerField', [], {}),
            'p_value': ('django.db.models.fields.FloatField', [], {}),
            'rat_cardiac': ('django.db.models.fields.FloatField', [], {}),
            'rat_extraocular': ('django.db.models.fields.FloatField', [], {}),
            'rat_glia': ('django.db.models.fields.FloatField', [], {}),
            'rat_hippocampal_ca1_1': ('django.db.models.fields.FloatField', [], {}),
            'rat_hippocampal_ca1_2': ('django.db.models.fields.FloatField', [], {}),
            'rat_hippocampus': ('django.db.models.fields.FloatField', [], {}),
            'rat_larynge': ('django.db.models.fields.FloatField', [], {}),
            'rat_muscle': ('django.db.models.fields.FloatField', [], {}),
            'rat_oculomotor': ('django.db.models.fields.FloatField', [], {}),
            'rat_spinal': ('django.db.models.fields.FloatField', [], {}),
            'rat_stromal': ('django.db.models.fields.FloatField', [], {}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'expressions.agingtranscriptome': {
            'Meta': {'object_name': 'AgingTranscriptome'},
            'changes_in_aging': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'chromosome': ('django.db.models.fields.IntegerField', [], {}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '162'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rna_nucleotide_accession_version': ('django.db.models.fields.CharField', [], {'max_length': '219', 'blank': 'True'}),
            'unigene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'expressions.cc3': {
            'Meta': {'object_name': 'Cc3'},
            'ac24_avg': ('django.db.models.fields.FloatField', [], {}),
            'ac24_max': ('django.db.models.fields.FloatField', [], {}),
            'affymetrix_probe_id_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_cc_f': ('django.db.models.fields.FloatField', [], {}),
            'anova_cc_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'cycling': ('django.db.models.fields.CharField', [], {'max_length': '54'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression_avg': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_cc': ('django.db.models.fields.FloatField', [], {}),
            'fourier_f24': ('django.db.models.fields.FloatField', [], {}),
            'fourier_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.FloatField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'ws195_wormbase_goterm_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'expressions.cd': {
            'Meta': {'object_name': 'Cd'},
            'adg': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'aor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'atr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'bat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'bon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'hat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kid': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'liv': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'num_tissue': ('django.db.models.fields.IntegerField', [], {}),
            'peak_mean': ('django.db.models.fields.FloatField', [], {}),
            'pfr': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'range_p': ('django.db.models.fields.FloatField', [], {}),
            'scn': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'skm': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ven': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'wat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'wb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'expressions.crsignature': {
            'Meta': {'object_name': 'CrSignature'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'overexp': ('django.db.models.fields.IntegerField', [], {}),
            'p_value': ('django.db.models.fields.FloatField', [], {}),
            'total': ('django.db.models.fields.IntegerField', [], {}),
            'underexp': ('django.db.models.fields.IntegerField', [], {})
        },
        'expressions.crtranscriptome': {
            'Meta': {'object_name': 'CrTranscriptome'},
            'changes_in_cr': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'chromosome': ('django.db.models.fields.IntegerField', [], {}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rna_nucleotide_accession_version': ('django.db.models.fields.CharField', [], {'max_length': '155', 'blank': 'True'}),
            'unigene_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'expressions.dd': {
            'Meta': {'object_name': 'Dd'},
            'affymetrix_probe_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_f_stat': ('django.db.models.fields.FloatField', [], {}),
            'anova_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'ct_number': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'genbank_accession_number': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'expressions.dd3': {
            'Meta': {'object_name': 'Dd3'},
            'ac24_avg': ('django.db.models.fields.FloatField', [], {}),
            'ac24_max': ('django.db.models.fields.FloatField', [], {}),
            'affymetrix_probe_id_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_f': ('django.db.models.fields.FloatField', [], {}),
            'anova_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'cycling': ('django.db.models.fields.CharField', [], {'max_length': '54'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression_avg': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_dd': ('django.db.models.fields.FloatField', [], {}),
            'fourier_f24': ('django.db.models.fields.FloatField', [], {}),
            'fourier_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.FloatField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'ws195_wormbase_gene_goterm_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'expressions.fastinginducedgenes': {
            'Meta': {'object_name': 'FastingInducedGenes'},
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ncbi_kogs': ('django.db.models.fields.CharField', [], {'max_length': '66', 'blank': 'True'})
        },
        'expressions.imprintedgenenetwork': {
            'Meta': {'object_name': 'ImprintedGeneNetwork'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'consistency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change_higher_as_5': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'heart_fold_change_1_to_4wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'heart_p_value_1_to_4wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kidney_fold_change_1_to_4wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'kidney_fold_change_1_to_8wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'kidney_p_value_1_to_4wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'kidney_p_value_1_to_8wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lung_fold_change_1_to_4wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lung_fold_change_1_to_8wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lung_p_value_1_to_4wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lung_p_value_1_to_8wk': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'p_value': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'expressions.juvenileinduced': {
            'Meta': {'object_name': 'JuvenileInduced'},
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '94'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'heart': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kidney': ('django.db.models.fields.FloatField', [], {}),
            'lung': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'probe_set': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'expressions.juvenilesuppressed': {
            'Meta': {'object_name': 'JuvenileSuppressed', 'db_table': "u'finkelstein2009_js'"},
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '99'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'heart': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kidney': ('django.db.models.fields.FloatField', [], {}),
            'lung': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'probe_set': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'expressions.ld': {
            'Meta': {'object_name': 'Ld'},
            'affymetrix_probe_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_f_stat': ('django.db.models.fields.FloatField', [], {}),
            'anova_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'ct_number': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'genbank_accession_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'expressions.ld3': {
            'Meta': {'object_name': 'Ld3'},
            'ac24_avg': ('django.db.models.fields.FloatField', [], {}),
            'ac24_max': ('django.db.models.fields.FloatField', [], {}),
            'affymetrix_probe_id_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_f': ('django.db.models.fields.FloatField', [], {}),
            'anova_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'cycling': ('django.db.models.fields.CharField', [], {'max_length': '54'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression_avg': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_ld': ('django.db.models.fields.FloatField', [], {}),
            'fourier_f24': ('django.db.models.fields.FloatField', [], {}),
            'fourier_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.FloatField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'ws195_wormbase_goterm_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'expressions.lddd6': {
            'Meta': {'object_name': 'Lddd6'},
            'ac24_avg': ('django.db.models.fields.FloatField', [], {}),
            'ac24_max': ('django.db.models.fields.FloatField', [], {}),
            'affymetrix_probe_id_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_dd_f': ('django.db.models.fields.FloatField', [], {}),
            'anova_dd_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'cycling': ('django.db.models.fields.CharField', [], {'max_length': '52'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression_avg': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_dd': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_ld': ('django.db.models.fields.FloatField', [], {}),
            'fourier_f24': ('django.db.models.fields.FloatField', [], {}),
            'fourier_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.FloatField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'ws195_wormbase_goterm_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'expressions.lin2002': {
            'Meta': {'object_name': 'Lin2002'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '223', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'hap4oe1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hap4oe2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hxk2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'low_glucose1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'low_glucose2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'expressions.postnatalgeneticprogram': {
            'Meta': {'object_name': 'PostnatalGeneticProgram', 'db_table': "u'postnatal_genetic_program'"},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change_from_1_to_4_wk_mouse_heart': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_from_1_to_4_wk_mouse_kidney': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_from_1_to_4_wk_mouse_lung': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_from_1_to_5_wk_rat_kidney': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_from_1_to_5_wk_rat_lung': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_from_1_to_8_wk_mouse_kidney': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_from_1_to_8_wk_mouse_lung': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'p_value_1_vs_4_wk_mouse_heart': ('django.db.models.fields.FloatField', [], {}),
            'p_value_1_vs_4_wk_mouse_kidney': ('django.db.models.fields.FloatField', [], {}),
            'p_value_1_vs_4_wk_mouse_lung': ('django.db.models.fields.FloatField', [], {}),
            'p_value_1_vs_5_wk_rat_kidney': ('django.db.models.fields.FloatField', [], {}),
            'p_value_1_vs_5_wk_rat_lung': ('django.db.models.fields.FloatField', [], {}),
            'p_value_1_vs_8_wk_mouse_kidney': ('django.db.models.fields.FloatField', [], {}),
            'p_value_1_vs_8_wk_mouse_lung': ('django.db.models.fields.FloatField', [], {})
        },
        'expressions.rapamycin': {
            'Meta': {'object_name': 'Rapamycin'},
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fpr1_8_rapamycin_mean': ('django.db.models.fields.FloatField', [], {}),
            'fpr1_8_rapamycin_replicate_1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fpr1_8_rapamycin_replicate_2': ('django.db.models.fields.FloatField', [], {}),
            'fpr1_8_rapamycin_replicate_3': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ly_83583_mean': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ly_83583_replicate_1': ('django.db.models.fields.FloatField', [], {}),
            'ly_83583_replicate_2': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'rapamycin_mean': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rapamycin_replicate_1': ('django.db.models.fields.FloatField', [], {}),
            'rapamycin_replicate_2': ('django.db.models.fields.FloatField', [], {})
        },
        'expressions.rapamycin_protein': {
            'Meta': {'object_name': 'rapamycin_protein'},
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'protein': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'protein_function': ('django.db.models.fields.CharField', [], {'max_length': '82'})
        },
        'expressions.sip2delta_aging': {
            'Meta': {'object_name': 'sip2delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '172'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'})
        },
        'expressions.sip2delta_wt': {
            'Meta': {'object_name': 'sip2delta_wt'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '178'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '38', 'blank': 'True'})
        },
        'expressions.snf4delta_aging': {
            'Meta': {'object_name': 'snf4delta_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '155'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '29', 'blank': 'True'})
        },
        'expressions.snf4delta_wt': {
            'Meta': {'object_name': 'snf4delta_wt'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'expressions.swindell2009': {
            'Meta': {'object_name': 'Swindell2009'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.CharField', [], {'max_length': '172', 'blank': 'True'}),
            'p_value': ('django.db.models.fields.FloatField', [], {}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        },
        'expressions.wc5': {
            'Meta': {'object_name': 'Wc5'},
            'ac24_avg': ('django.db.models.fields.FloatField', [], {}),
            'ac24_max': ('django.db.models.fields.FloatField', [], {}),
            'affymetrix_probe_id_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_f': ('django.db.models.fields.FloatField', [], {}),
            'anova_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'cycling': ('django.db.models.fields.CharField', [], {'max_length': '54'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression_avg': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_wc': ('django.db.models.fields.FloatField', [], {}),
            'fourier_f24': ('django.db.models.fields.FloatField', [], {}),
            'fourier_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.FloatField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'ws195_wormbase_goterm_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'expressions.wccc6': {
            'Meta': {'object_name': 'Wccc6'},
            'ac24_avg': ('django.db.models.fields.FloatField', [], {}),
            'ac24_max': ('django.db.models.fields.FloatField', [], {}),
            'affymetrix_probe_id_set': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'anova_cc_f': ('django.db.models.fields.FloatField', [], {}),
            'anova_cc_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'cycling': ('django.db.models.fields.CharField', [], {'max_length': '52'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression_avg': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_cc': ('django.db.models.fields.FloatField', [], {}),
            'fold_change_wc': ('django.db.models.fields.FloatField', [], {}),
            'fourier_f24': ('django.db.models.fields.FloatField', [], {}),
            'fourier_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phase': ('django.db.models.fields.FloatField', [], {}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'ws195_wormbase_goterm_info': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'expressions.wt_aging': {
            'Meta': {'object_name': 'wt_aging'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '146'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fold_change': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_process': ('django.db.models.fields.CharField', [], {'max_length': '56'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'specific_process': ('django.db.models.fields.CharField', [], {'max_length': '54', 'blank': 'True'})
        },
        'expressions.wtcrvsyepd1': {
            'Meta': {'object_name': 'wtcrvsyepd1'},
            'al': ('django.db.models.fields.FloatField', [], {}),
            'dr': ('django.db.models.fields.FloatField', [], {}),
            'dr_al': ('django.db.models.fields.FloatField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['expressions']
