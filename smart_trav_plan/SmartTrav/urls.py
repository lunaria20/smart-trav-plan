from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),


# Forgot Password (new additions using Django's built-in views)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Itinerary
    path('itinerary/create/', views.create_itinerary, name='create_itinerary'),

    # Expenses
    path('expense/add/', views.add_expense, name='add_expense'),

    # Profile
    path('profile/update/', views.update_profile, name='update_profile'),

    path('about/', views.about_view, name='about'),
    path('service/', views.service_view, name='service'),

]