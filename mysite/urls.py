"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.sitemaps.views import sitemap
from website.sitesmaps import StaticViewSitemap
from blog.sitemap import BlogPostSitemap, BlogCategorySitemap, BlogStaticSitemap
import debug_toolbar

sitemaps = {
    'static': StaticViewSitemap,
    'blog-posts': BlogPostSitemap,
    'blog-categories': BlogCategorySitemap,
    'blog-static': BlogStaticSitemap,
}

urlpatterns = [
    # استفاده از پنل ادمین اصلی جنگو با کپچا
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('blog/', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('captcha/', include('captcha.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def handler404(request, exception):
    return render(request, '404.html', status=404)
