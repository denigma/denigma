from django_easyfilters import FilterSet
from django.utils.safestring import mark_safe


FilterSet.template = u"""<li>
<div class="filterline"><span class="filterlabel">{{ filterlabel }}:</span>
<a href="#{{ filterlabel }}-show" id="{{ filterlabel }}-show" class="show">+</a>
<a href="#{{ filterlabel }}-hide" id="{{ filterlabel }}-hide" class="hide">-</a>
<div class="collapsing">
{% for choice in choices %}
  {% if choice.link_type == 'add' %}
    <span class="addfilter"><a href="{{ choice.url }}" title="Add filter">{{ choice.label }}&nbsp;({{ choice.count }})</a></span>&nbsp;&nbsp;
  {% else %}
    {% if choice.link_type == 'remove' %}
    <span class="removefilter"><a href="{{ choice.url }}" title="Remove filter">{{ choice.label }}&nbsp;&laquo;&nbsp;</a></span>
    {% else %}
      <span class="displayfilter">{{ choice.label }}</span>
    {% endif %}
  {% endif %}
{% endfor %}
           </div>
</div></li>
"""

class VariantFilterSet(FilterSet):
    fields = ['ethnicity', 'study_type',
              'variant_type',
              'classifications',
              #'or_type', 'significant', 'finding', 'created', 'updated'
              ] #, 'location'] #, 'choice',   'technology']
    hidden = []#'ethnicity'

    def render(self):
        return mark_safe(u'\n'.join(self.render_filter(f) for f in self.filters if f.field not in self.hidden))