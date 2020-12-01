from django.contrib.sitemaps import Sitemap
# from django.core.urlresolvers import reverse
from django.urls import reverse

from .models import Post

class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home', 'latest-posts']

    def location(self, item):
        return reverse(item)

class Post_Sitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Post.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj): 
        return obj.created