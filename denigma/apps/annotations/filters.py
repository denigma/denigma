from django_easyfilters import FilterSet


class TissueFilterSet(FilterSet):
    fields = ('hierarchy',)

class GOFilterSet(FilterSet):
    fields = ('taxid', 'evidence', 'qualifier')