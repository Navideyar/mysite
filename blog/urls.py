from django.urls import path
from blog.views import blog_view, blog_single, test, blog_category, blog_search

app_name = "blog"

urlpatterns = [
    path("", blog_view, name="index"),
    path("<int:pid>", blog_single, name="single"),
    path("test", test, name="test"),
    path("category/<str:cat_name>/", blog_category, name="category"),
    path("search/", blog_search, name="search"),
    path("author/<str:author_username>/", blog_view, name="author"),
]