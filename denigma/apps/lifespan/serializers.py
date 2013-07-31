from rest_framework import serializers

from models import Factor #, Type


class FactorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Factor
        fields = ('id', 'entrez_gene_id', 'ensembl_gene_id', 'symbol', 'name', 'alias',
                  'functional_description',
                  'observation',
                  #'taxid',
                  'species',
                  #'pubmed_id', 'reference',
                  #'mean', 'median', 'maximum', '_75', '_25',
                  #'manipulation', 'gene_intervention', 'human_homologue',
                  # 'note', 'type', #'pdb',
                  #'classification',
                  'types',
                  'intervention',
                  'classifications',
                  'references'
        )

# class TypeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Type
#         fields = ('name', )