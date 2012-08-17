# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Interactome9606'
        db.delete_table('interactions_interactome9606')

        # Deleting model 'Interactome6239'
        db.delete_table('interactions_interactome6239')

        # Deleting model 'Interactome10090'
        db.delete_table('interactions_interactome10090')

        # Deleting model 'Interactome7227'
        db.delete_table('interactions_interactome7227')

        # Deleting model 'Interactome4932'
        db.delete_table('interactions_interactome4932')


    def backwards(self, orm):
        
        # Adding model 'Interactome9606'
        db.create_table('interactions_interactome9606', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=134)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=88, blank=True)),
            ('pmid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome9606'])

        # Adding model 'Interactome6239'
        db.create_table('interactions_interactome6239', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=104)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=174, blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('pmid', self.gf('django.db.models.fields.CharField')(max_length=94, blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome6239'])

        # Adding model 'Interactome10090'
        db.create_table('interactions_interactome10090', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=38, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=73)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.CharField')(max_length=240, blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.CharField')(max_length=159, blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('pmid', self.gf('django.db.models.fields.CharField')(max_length=115, blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome10090'])

        # Adding model 'Interactome7227'
        db.create_table('interactions_interactome7227', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('source_database', self.gf('django.db.models.fields.CharField')(max_length=95)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('pmid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome7227'])

        # Adding model 'Interactome4932'
        db.create_table('interactions_interactome4932', (
            ('interactor_a', self.gf('django.db.models.fields.IntegerField')()),
            ('interactor_b', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('experimental_system_type', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('source_database', self.gf('django.db.models.fields.TextField')()),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('interaction_detection_method', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interaction_type', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modification', self.gf('django.db.models.fields.CharField')(max_length=54, blank=True)),
            ('pmid', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('interactions', ['Interactome4932'])


    models = {
        'interactions.biogrid': {
            'Meta': {'object_name': 'Biogrid'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '37'}),
            'biogrid_id_interactor_a': ('django.db.models.fields.IntegerField', [], {}),
            'biogrid_id_interactor_b': ('django.db.models.fields.IntegerField', [], {}),
            'biogrid_interaction_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'entrez_gene_interactor_a': ('django.db.models.fields.IntegerField', [], {}),
            'entrez_gene_interactor_b': ('django.db.models.fields.IntegerField', [], {}),
            'experimental_system': ('django.db.models.fields.CharField', [], {'max_length': '29'}),
            'experimental_system_type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'modification': ('django.db.models.fields.CharField', [], {'max_length': '22'}),
            'official_symbol_interactor_a': ('django.db.models.fields.CharField', [], {'max_length': '21'}),
            'official_symbol_interactor_b': ('django.db.models.fields.CharField', [], {'max_length': '31'}),
            'organism_interactor_a': ('django.db.models.fields.IntegerField', [], {}),
            'organism_interactor_b': ('django.db.models.fields.IntegerField', [], {}),
            'phenotypes': ('django.db.models.fields.CharField', [], {'max_length': '209'}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {}),
            'qualifications': ('django.db.models.fields.TextField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'source_database': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'synonymns_interactor_a': ('django.db.models.fields.TextField', [], {}),
            'synonyms_interactor_b': ('django.db.models.fields.TextField', [], {}),
            'systematic_name_interactor_a': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'systematic_name_interactor_b': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'throughput': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'interactions.fly_tf_gene': {
            'Meta': {'object_name': 'Fly_TF_gene'},
            'data_source_url': ('django.db.models.fields.CharField', [], {'max_length': '67'}),
            'data_version': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date_last_updated': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'fly_target_gene': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'fly_tf_gene': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'gene_symbol': ('django.db.models.fields.CharField', [], {'max_length': '29'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interaction_detect_methods': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'interaction_source': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'interaction_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pmid_method': ('django.db.models.fields.CharField', [], {'max_length': '168'}),
            'pmid_url': ('django.db.models.fields.CharField', [], {'max_length': '119'}),
            'pubmedid': ('django.db.models.fields.CharField', [], {'max_length': '33'}),
            'source': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'source_mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'target_mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tf_symbol': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'url_factor': ('django.db.models.fields.CharField', [], {'max_length': '67'})
        },
        'interactions.mirecord': {
            'Meta': {'object_name': 'miRecord'},
            'additional_note': ('django.db.models.fields.CharField', [], {'max_length': '141', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mirna_mature_id': ('django.db.models.fields.CharField', [], {'max_length': '18', 'blank': 'True'}),
            'mirna_regulation': ('django.db.models.fields.CharField', [], {'max_length': '66', 'blank': 'True'}),
            'mirna_regulation_site': ('django.db.models.fields.CharField', [], {'max_length': '63', 'blank': 'True'}),
            'mirna_species': ('django.db.models.fields.CharField', [], {'max_length': '37', 'blank': 'True'}),
            'mutation_target_region': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'mutation_target_site': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'original_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_description_inter_site': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_description_mutation_region': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'original_description_mutation_site': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'post_mutation_method': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            'post_mutation_method_site': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'}),
            'pubmed_id': ('django.db.models.fields.IntegerField', [], {}),
            'reporter_link_element1': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'reporter_link_element2': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'reporter_target_gene_region': ('django.db.models.fields.CharField', [], {'max_length': '26', 'blank': 'True'}),
            'reporter_target_site': ('django.db.models.fields.CharField', [], {'max_length': '26', 'blank': 'True'}),
            'target_gene_mrna_level': ('django.db.models.fields.CharField', [], {'max_length': '9', 'blank': 'True'}),
            'target_gene_name': ('django.db.models.fields.CharField', [], {'max_length': '44', 'blank': 'True'}),
            'target_gene_refseq_acc': ('django.db.models.fields.CharField', [], {'max_length': '14', 'blank': 'True'}),
            'target_gene_species_common': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'target_gene_species_scientific': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'target_site_number': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'target_site_position': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'test_method_inter': ('django.db.models.fields.CharField', [], {'max_length': '34', 'blank': 'True'}),
            'test_method_inter_site': ('django.db.models.fields.CharField', [], {'max_length': '27', 'blank': 'True'})
        },
        'interactions.modelling': {
            'Meta': {'object_name': 'Modelling'},
            'creation_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interaction_type': ('django.db.models.fields.CharField', [], {'max_length': '159', 'blank': 'True'}),
            'interactor_a': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'interactor_b': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pmid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'taxid': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'interactions.tnet': {
            'Meta': {'object_name': 'tnet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'tg': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'interactions.yeast_tf_chip_chip': {
            'Meta': {'object_name': 'Yeast_TF_ChIP_chip'},
            'a1_mata1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'abf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'abt1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'aca1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ace2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'adr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'aft2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'arg80': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'arg81': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'aro80': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'arr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ash1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ask10': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'azf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'bas1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'bye1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'cad1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'cbf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'cha4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'cin5': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'crz1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'cst6': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'cup9': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dal80': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dal81': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dal82': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dat1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dig1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'dot6': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ecm22': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'eds1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fap7': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fhl1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fkh1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fkh2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'fzf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gal3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gal4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gal80': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gat1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gat3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gcn4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gcr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gcr2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gln3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gts1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'gzf3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'haa1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hac1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hal9': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hap1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hap2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hap3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hap4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hap5': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hir1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hir2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hir3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hms1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hms2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hog1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'hsf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ifh1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ime1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ime4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ino2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ino4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ixr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'kre33': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'kss1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'leu3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mac1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mal13': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mal33': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mbf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mbp1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mcm1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mds3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'met18': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'met28': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'met31': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'met32': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'met4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mga1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mig1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mig2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mig3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mot3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'msn1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'msn2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'msn4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mss11': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'mth1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '148', 'blank': 'True'}),
            'ndd1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ndt80': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'nnf2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'nrg1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'oaf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'opi1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'orf': ('django.db.models.fields.CharField', [], {'max_length': '31', 'blank': 'True'}),
            'pdc2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'pdr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'pdr3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'phd1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'pho2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'pho4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'pip2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ppr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'put3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rap1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rco1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rcs1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rdr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rds1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'reb1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rfx1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rgm1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rgt1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rim101': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rlm1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rlr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rme1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rox1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rph1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rpi1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rpn4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rtg1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rtg3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'rts2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sfl1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sfp1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sig1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sip3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sip4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'skn7': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sko1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'smk1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'smp1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'snf1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'snt2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sok2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'spt10': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'spt2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'spt23': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'srd1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stb1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stb2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stb4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stb5': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stb6': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ste12': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stp1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stp2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'stp4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sum1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sut1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'sut2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'swi4': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'swi5': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'swi6': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'tbs1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'tec1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'thi2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'tos8': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'tye7': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'uga3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ume6': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'upc2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'usv1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'war1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'wtm1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'wtm2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'xbp1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yap1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yap3': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yap5': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yap6': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yap7': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ybl054w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ybr239c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ybr267w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ydr026c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ydr049w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ydr266c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ydr520c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yer051w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yer130c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yer184c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yfl044c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yfl052w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ygr067c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yhp1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yjl206c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ykl222c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ykr064w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ylr278c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yml081w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ynr063w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yox1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ypr022c': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'ypr196w': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'yrr1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'zap1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'zms1': ('django.db.models.fields.FloatField', [], {'blank': 'True'})
        },
        'interactions.yeastract': {
            'Meta': {'object_name': 'Yeastract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source_mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'target_gene': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'target_mapping': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tf': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['interactions']
