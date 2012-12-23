from django_easyfilters import FilterSet


class ProfileFilterSet(FilterSet):
    fields = ('country', 'gender')
