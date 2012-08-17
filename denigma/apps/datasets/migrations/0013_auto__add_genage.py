# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'GenAge'
        db.create_table('datasets_genage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entrez_gene_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mapping', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('ensembl_gene_id', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
            ('gene_symbol', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('gene_name', self.gf('django.db.models.fields.CharField')(max_length=244, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('taxid', self.gf('django.db.models.fields.IntegerField')()),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=240, blank=True)),
            ('observation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('pubmed_id', self.gf('django.db.models.fields.CharField')(max_length=19, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=42)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('synergistic_epistasis', self.gf('django.db.models.fields.CharField')(max_length=33, blank=True)),
            ('antagonistic_epistasis', self.gf('django.db.models.fields.CharField')(max_length=216, blank=True)),
            ('human_homologue', self.gf('django.db.models.fields.CharField')(max_length=18, blank=True)),
        ))
        db.send_create_signal('datasets', ['GenAge'])


    def backwards(self, orm):
        
        # Deleting model 'GenAge'
        db.delete_table('datasets_genage')


    models = {
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
            'observation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '19', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'synergistic_epistasis': ('django.db.models.fields.CharField', [], {'max_length': '33', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
        },
        'datasets.gendr': {
            'Meta': {'object_name': 'Gendr'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'ensembl_gene_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'entrez_gene_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'gene_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.CharField', [], {'max_length': '87', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {})
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
