from django_easyfilters import FilterSet


class TissueFilterSet(FilterSet):
    fields = ('hierarchy',)