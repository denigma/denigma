from django_easyfilters import FilterSet


class LinkFilterSet(FilterSet):
    fields = ('language', 'creation', 'category')
