from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Itinerary
    path('itinerary/create/', views.create_itinerary, name='create_itinerary'),

    # Expenses
    path('expense/add/', views.add_expense, name='add_expense'),

    # Profile
    path('profile/update/', views.update_profile, name='update_profile'),
]