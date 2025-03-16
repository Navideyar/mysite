from django.urls import path
from .views import *

app_name = "website"

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("category/<str:cat_name>/", blog_category, name="category"),
    path("contact/", contact, name="contact"),
    path("newsletter/", newsletter_view, name="newsletter"),
]
