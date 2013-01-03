from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^labs/?', 'links.views.newLink', name="new-link"),
    url(r'^category/?$', 'links.views.newCategory', name="new-category"),
    url(r'^countries/?$', 'links.views.newCountry', name="new-country"),
    url(r'^contacts/?', 'experts.views.newProfile', name="new-profile"),
    url(r'^members/?', 'experts.views.newProfile', name='new-member'),
    url(r'^project/?', 'data.views.newEntry', name='new-entry'),
    url(r'intervention/?', 'lifespan.views.newIntervention', name='new-intervention'),
    url(r'alternative_names/?', 'annotations.views.newAnimal', name="new-animal"),
    url(r'images/?', 'media.views.newImage', name="new-images")
)