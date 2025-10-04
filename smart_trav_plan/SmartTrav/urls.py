from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

# Serve media files during development

urlpatterns = [
    path('admin/', admin.site.urls),

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

    path('destination/add-to-trip/', views.add_destination_to_trip, name='add_destination_to_trip'),

    # Expenses
    path('expense/add/', views.add_expense, name='add_expense'),

    # Profile
    path('profile/update/', views.update_profile, name='update_profile'),

    path('about/', views.about_view, name='about'),
    path('service/', views.service_view, name='service'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

