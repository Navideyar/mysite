from django.contrib.sitemaps import Sitemap
from blog.models import Post, Category
from django.urls import reverse

class BlogPostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status=True)

    def lastmod(self, obj):
        return obj.updated_date

    def location(self, obj):
        return reverse('blog:single', kwargs={'pid': obj.id})

class BlogCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('blog:category', kwargs={'cat_name': obj.name})

class BlogStaticSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return ['blog:index', 'blog:search']

    def location(self, item):
        return reverse(item)
