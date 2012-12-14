from django_easyfilters import FilterSet


class InteractionFilterSet(FilterSet):
    fields = ('taxid_a', 'taxid_b')