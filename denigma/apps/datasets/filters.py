from django_easyfilters import FilterSet


class ReferenceFilterSet(FilterSet):
    fields = ('year', 'label', 'categories')