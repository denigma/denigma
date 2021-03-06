# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Intervention'
        db.delete_table('datasets_intervention')

        # Removing M2M table for field intervention on 'GenAge'
        db.delete_table('datasets_genage_intervention')


    def backwards(self, orm):
        
        # Adding model 'Intervention'
        db.create_table('datasets_intervention', (
            ('background', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('manipulation', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('pmid', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('mean', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('median', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('effect', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('maximum', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('datasets', ['Intervention'])

        # Adding M2M table for field intervention on 'GenAge'
        db.create_table('datasets_genage_intervention', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genage', models.ForeignKey(orm['datasets.genage'], null=False)),
            ('intervention', models.ForeignKey(orm['datasets.intervention'], null=False))
        ))
        db.create_unique('datasets_genage_intervention', ['genage_id', 'intervention_id'])


    models = {
        'datasets.acetylation': {
            'Meta': {'object_name': 'Acetylation'},
            'ensembl_gene': ('django.db.models.fields.CharField', [], {'max_length': '9', 'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'h2ak7': ('django.db.models.fields.FloatField', [], {}),
            'h2bk11': ('django.db.models.fields.FloatField', [], {}),
            'h2bk16': ('django.db.models.fields.FloatField', [], {}),
            'h3k14': ('django.db.models.fields.FloatField', [], {}),
            'h3k18': ('django.db.models.fields.FloatField', [], {}),
            'h3k23': ('django.db.models.fields.FloatField', [], {}),
            'h3k27': ('django.db.models.fields.FloatField', [], {}),
            'h3k9': ('django.db.models.fields.FloatField', [], {}),
            'h4k12': ('django.db.models.fields.FloatField', [], {}),
            'h4k16': ('django.db.models.fields.FloatField', [], {}),
            'h4k8': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'datasets.adult_height_association': {
            'Meta': {'object_name': 'Adult_Height_Association'},
            'chr': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'effect_allele': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'female_effect': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'female_p': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_rank': ('django.db.models.fields.IntegerField', [], {}),
            'male_effect': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'male_p': ('django.db.models.fields.FloatField', [], {}),
            'phet_m_vs_f': ('django.db.models.fields.FloatField', [], {}),
            'snp': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'datasets.adultheightassociation': {
            'Meta': {'object_name': 'AdultHeightAssociation'},
            'chr': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'effect_allele': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'female_effect': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'female_p': ('django.db.models.fields.FloatField', [], {}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_rank': ('django.db.models.fields.IntegerField', [], {}),
            'male_effect': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'male_p': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phet_m_vs_f': ('django.db.models.fields.FloatField', [], {}),
            'snp': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'datasets.bmal1_sites_liver': {
            'Meta': {'object_name': 'BMAL1_Sites_Liver'},
            'biotype': ('django.db.models.fields.CharField', [], {'max_length': '23'}),
            'chromosome': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'conservation': ('django.db.models.fields.FloatField', [], {}),
            'distance': ('django.db.models.fields.IntegerField', [], {}),
            'e1': ('django.db.models.fields.IntegerField', [], {}),
            'e1_e2': ('django.db.models.fields.IntegerField', [], {}),
            'end': ('django.db.models.fields.IntegerField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mrna_phase': ('django.db.models.fields.FloatField', [], {}),
            'mrna_pvalue': ('django.db.models.fields.FloatField', [], {}),
            'start': ('django.db.models.fields.IntegerField', [], {}),
            'zt10': ('django.db.models.fields.IntegerField', [], {}),
            'zt14': ('django.db.models.fields.IntegerField', [], {}),
            'zt18': ('django.db.models.fields.IntegerField', [], {}),
            'zt2': ('django.db.models.fields.IntegerField', [], {}),
            'zt22': ('django.db.models.fields.IntegerField', [], {}),
            'zt6': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.circadiansystemicentrainedfactors': {
            'Meta': {'object_name': 'CircadianSystemicEntrainedFactors'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'datasets.clockmodulator': {
            'Meta': {'object_name': 'ClockModulator'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'confirmed_by_bmal1_kockdown': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '152'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phenotype': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'rna_nucleotide_accession_version': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        'datasets.dam_fernandez2011': {
            'Meta': {'object_name': 'DAM_Fernandez2011'},
            'cgi': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'correlation': ('django.db.models.fields.FloatField', [], {}),
            'cpg_site': ('django.db.models.fields.CharField', [], {'max_length': '19'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'p_value': ('django.db.models.fields.FloatField', [], {})
        },
        'datasets.genage': {
            'Meta': {'object_name': 'GenAge'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'antagonistic_epistasis': ('django.db.models.fields.CharField', [], {'max_length': '216', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '244', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'human_homologue': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'maximum': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'mean': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'median': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '19', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'synergistic_epistasis': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.gencc': {
            'Meta': {'object_name': 'GenCC'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '68', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.CharField', [], {'max_length': '248', 'blank': 'True'}),
            'peak_actvity': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'peak_mrna': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'peak_protein': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '37', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.gendr': {
            'Meta': {'object_name': 'Gendr'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lifespan': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datasets.Lifespan']", 'symmetrical': 'False'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '87', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'regimen': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['datasets.Regimen']", 'symmetrical': 'False'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.humanbraindnamethylationchanges': {
            'Meta': {'object_name': 'HumanBrainDnaMethylationChanges'},
            'adjusted_r2_estimates_from_stage_i_crblm': ('django.db.models.fields.FloatField', [], {}),
            'adjusted_r2_estimates_from_stage_i_fctx': ('django.db.models.fields.FloatField', [], {}),
            'adjusted_r2_estimates_from_stage_i_pons': ('django.db.models.fields.FloatField', [], {}),
            'adjusted_r2_estimates_from_stage_i_tctx': ('django.db.models.fields.FloatField', [], {}),
            'beta_coefficient_range': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'c_g_count': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'chr': ('django.db.models.fields.IntegerField', [], {}),
            'cpg_count': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'cpg_sequence': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'cpg_sequence_2kb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'distance_to_tss': ('django.db.models.fields.IntegerField', [], {}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'genomic_position_in_bp': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'percentage_c_or_g': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'percentage_cpg': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'ratio': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'stage_i_pvalue_crblm': ('django.db.models.fields.FloatField', [], {}),
            'stage_i_pvalue_fctx': ('django.db.models.fields.FloatField', [], {}),
            'stage_i_pvalue_pons': ('django.db.models.fields.FloatField', [], {}),
            'stage_i_pvalue_tctx': ('django.db.models.fields.FloatField', [], {}),
            'stage_ii_pvalue_crblm': ('django.db.models.fields.FloatField', [], {}),
            'stage_ii_pvalue_fctx': ('django.db.models.fields.FloatField', [], {})
        },
        'datasets.humangenes': {
            'Meta': {'object_name': 'HumanGenes'},
            'aliases': ('django.db.models.fields.CharField', [], {'max_length': '68', 'blank': 'True'}),
            'band': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'cds_accession': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'}),
            'cellular_location': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'epd_accession': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'expression': ('django.db.models.fields.CharField', [], {'max_length': '69'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '94'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '131'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hagrid': ('django.db.models.fields.IntegerField', [], {}),
            'homologene': ('django.db.models.fields.IntegerField', [], {}),
            'homologues': ('django.db.models.fields.TextField', [], {}),
            'hprd': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interactions': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location_end': ('django.db.models.fields.IntegerField', [], {}),
            'location_start': ('django.db.models.fields.IntegerField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observations': ('django.db.models.fields.TextField', [], {}),
            'omim': ('django.db.models.fields.IntegerField', [], {}),
            'orf_accession': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'orientation': ('django.db.models.fields.IntegerField', [], {}),
            'pubmed_ids': ('django.db.models.fields.TextField', [], {}),
            'reference': ('django.db.models.fields.TextField', [], {}),
            'selection_reason': ('django.db.models.fields.CharField', [], {'max_length': '21'}),
            'swiss_prot': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'unigene': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.joannegenes': {
            'Meta': {'object_name': 'JoanneGenes'},
            'assoc_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cds_length': ('django.db.models.fields.IntegerField', [], {}),
            'chimp_ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '19'}),
            'chimp_percentage_id': ('django.db.models.fields.IntegerField', [], {}),
            'dn': ('django.db.models.fields.FloatField', [], {}),
            'dn_ds': ('django.db.models.fields.FloatField', [], {}),
            'ds': ('django.db.models.fields.FloatField', [], {}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'human_percentage_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longevity': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'datasets.k56ac': {
            'Meta': {'object_name': 'K56Ac'},
            'ensembl_gene': ('django.db.models.fields.CharField', [], {'max_length': '9', 'primary_key': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expression': ('django.db.models.fields.FloatField', [], {}),
            'level': ('django.db.models.fields.FloatField', [], {}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'datasets.lifespan': {
            'Meta': {'object_name': 'Lifespan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'datasets.murineimprinted': {
            'Meta': {'object_name': 'MurineImprinted'},
            'chromosome': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'chromosome_region': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expressed_parental_allele': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '74'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'datasets.newlongevityregulators': {
            'Meta': {'object_name': 'NewLongevityRegulators'},
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'phenotype': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        'datasets.newlongevityregulatorscandidates': {
            'Meta': {'object_name': 'NewLongevityRegulatorsCandidates'},
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wormbase_id': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'})
        },
        'datasets.pokholok': {
            'Meta': {'object_name': 'Pokholok'},
            'chr': ('django.db.models.fields.IntegerField', [], {}),
            'ensembl_gene': ('django.db.models.fields.CharField', [], {'max_length': '19'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'esa1_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gcn4_aa': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gcn5_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gg_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3_h2o2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k14acvsh3_h2o2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k14acvsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k14acvswce_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k36me3vsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k4me1vsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k4me2vsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k4me3vsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k79me3vsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h3k9acvsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h4_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h4acvsh3_h2o2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'h4acvsh3_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'noab_ypd': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'pos': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.regimen': {
            'Meta': {'object_name': 'Regimen'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'shortcut': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'datasets.survivinginthecold': {
            'Meta': {'object_name': 'SurvivingInTheCold'},
            'embl': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_tag': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'protein_accession_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sgd_id': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'datasets.ultradian': {
            'Meta': {'object_name': 'Ultradian'},
            'component': ('django.db.models.fields.CharField', [], {'max_length': '65', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '243'}),
            'f': ('django.db.models.fields.IntegerField', [], {}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '165', 'blank': 'True'}),
            'gene': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'o': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'process': ('django.db.models.fields.CharField', [], {'max_length': '225', 'blank': 'True'})
        }
    }

    complete_apps = ['datasets']
