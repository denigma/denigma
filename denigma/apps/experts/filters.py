from django_easyfilters import FilterSet


class ProfileFilterSet(FilterSet):
    fields = ('country', 'entries') # 'gender''collaboration'

class CollaborationFilterSet(FilterSet):
    fields = ('project', 'labs', 'members')
