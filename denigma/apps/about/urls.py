from django.conf.urls import patterns, url


urlpatterns = patterns("about.views",
    url(r'^$', 'index', name='about'),
    url(r"^what_next/$", 'what_next', {"template": "about/what_next.html"},
        name="what_next"),
    url(r"^matrix/$", 'matrix', {'number':0}, name='matrix'),
    url(r"^matrix/(?P<number>[\w]+)/$", 'matrix'),
    url(r"^matrix/(?P<number>[\w]+)/choice/(?P<color>[\w]+)", 'choice'),
)
urlpatterns += patterns("",
    url(r'^terms/$', 'django.contrib.flatpages.views.flatpage',
       kwargs={'url': '/about/terms/'},
       name='terms'),
    url(r'^privacy/$', 'django.contrib.flatpages.views.flatpage',
       kwargs={'url': '/about/privacy/'},
       name='privacy'),
)

#    url(r'^$', 'django.contrib.flatpages.views.flatpage',
#       kwargs={'url': '/about/'},
#       name='about'),

    #url(r"^$", direct_to_template, {"template": "about/index.html"}, 
    #    name="about"), # Depricated.
    #url(r"^terms/$", direct_to_template, {"template": "about/terms.html"},
    #    name="terms"), # Depricated.
    #url(r"^privacy/$", direct_to_template, {"template": "about/privacy.html"},
    #    name="privacy"), # Depricated.
    #url(r"^dmca/$", direct_to_template, {"template": "about/dmca.html"},
    #    name="dmca"), # Not used (What is it actually?).
    #url(r"^tutorial/$", direct_to_template, {"template": "about/tutorial.html"},
    #    name="tutorial"), # Depricated (moved to tutorials app).

#234567891123456789212345678931234567894123456789512345678961234567897123456789
