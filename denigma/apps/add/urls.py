from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^labs/?', 'links.views.newLink', name="new-link"),
    url(r'^category/?$', 'links.views.newCategory', name="new-category"),
    url(r'^countries/?$', 'links.views.newCountry', name="new-country"),
    url(r'^nation/?$', 'links.views.newCountry', name="new-country"),
    url(r'^contacts/?', 'experts.views.newProfile', name="new-profile"),
    url(r'^members/?', 'experts.views.newProfile', name='new-member'),
    url(r'^project/?', 'data.views.newEntry', name='new-entry'),
    url(r'^categories/?', 'data.views.newEntry', name='new-category'),
    url(r'intervention/?', 'lifespan.views.newIntervention', name='new-intervention'),
    url(r'factor/?', 'lifespan.views.newFactor', name='new-factor'),
    url(r'state/?', 'lifespan.views.newChoice', name='new-choice'),
    url(r'choice/?', 'lifespan.views.newChoice', name='new-choice'),
    url(r'alternative_names/?', 'annotations.views.newAnimal', name="new-animal"),
    url(r'images/?', 'media.views.newImage', name="new-images"),
    url(r'population/?', 'lifespan.views.newPopulation', name="new-population"),
    url(r'ethnicity/?', 'lifespan.views.newPopulation', name="new-population"),
    url(r'technology/?', 'lifespan.views.newTechnology', name="new-technology"),
    url(r'study_type/?', 'lifespan.views.newStudyType', name="new-study_type"),
    url(r'^reference/?', 'datasets.views.newReference', name="new-reference"),
    url(r'^classifications/?', 'annotations.views.newClassification', name="new-classification"),

)