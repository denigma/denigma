from datetime import datetime

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from apps.blog.models import Post


class SiteMap(Sitemap):
     changefreq = 'never'
     priority = 0.5

     def items(self):
         return Post.objects.filter(published=True)

     def lastmod(self, obj):
         return obj.updated

     def location(self, obj):
         return '/'


class SiteSiteMap(Sitemap):
     def __init__(self, names):
         self.names = names

     def items(self):
         return self.names

     def changefrq(self, obj):
         return 'weekly'

     def lastmod(self, obj):
         return datetime.now()

     def location(self, obj):
          return reverse(obj)
