from django_easyfilters import FilterSet


class LinkFilterSet(FilterSet):
    fields = ('language', 'countries', 'creation', 'category', 'categories') # 'site'
