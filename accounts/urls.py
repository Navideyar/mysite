from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin-redirect/', views.admin_redirect_view, name='admin_redirect'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    #path('register/', views.register_view, name='register'),
]

