from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['website:home', 'website:about', 'website:contact']

    def location(self, item):
        return reverse(item)