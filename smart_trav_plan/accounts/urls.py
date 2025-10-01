from django.urls import path
from .views import CustomLogoutView
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='SmartTrav/accounts/login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path(
        'logout/',
        LogoutView.as_view(next_page='/accounts/login/'),
        name='logout'
    ),
]
