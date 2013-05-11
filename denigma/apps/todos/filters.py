from django_easyfilters import FilterSet
from django_easyfilters.filters import Filter

class BooleanFilter(Filter):
    pass
#    def __init__(self, field, model, param, **kwargs):
#        super(BooleanFilter, self).__init__(self, field, model, param, **kwargs)


class TodoFilterSet(FilterSet):
    fields = (#'done',# {}, BooleanFilter),
              'categories',
              'creator',
              'executor',
              'priority',
              'difficulty',
              'value',
              'created',
              'updated',
              'start_date',
              'stop_date',
              'done',

              #'created', 'updated', 'start_date', 'stop_date'] #  rename to priority.
)