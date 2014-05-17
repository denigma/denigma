from django_easyfilters import FilterSet
from django.utils.safestring import mark_safe


class VariantFilterSet(FilterSet):
    fields = ['ethnicity', 'study_type',
              'variant_type',
              'classifications',
              #'or_type', 'significant', 'finding', 'created', 'updated'
              ] #, 'location'] #, 'choice',   'technology']
    hidden = []#'ethnicity'

    def render(self):
        return mark_safe(u'\n'.join(self.render_filter(f) for f in self.filters if f.field not in self.hidden))