from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    # Forgot Password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Itinerary (Trips)
    path('itinerary/create/', views.create_itinerary, name='create_itinerary'),
    path('itinerary/edit/<int:itinerary_id>/', views.edit_itinerary, name='edit_itinerary'),
    path('itinerary/delete/<int:itinerary_id>/', views.delete_itinerary, name='delete_itinerary'),
    path('itinerary/<int:itinerary_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('itinerary/<int:itinerary_id>/export-pdf/', views.export_itinerary_pdf, name='export_itinerary_pdf'),

    # Destinations
    path('destination/add-to-trip/', views.add_destination_to_trip, name='add_destination_to_trip'),
    path('destination/save/<int:destination_id>/', views.save_destination, name='save_destination'),
    path('destination/remove-saved/<int:destination_id>/', views.remove_saved_destination,
         name='remove_saved_destination'),

    # Destination Actions
    path('destination/remove-from-trip/<int:itinerary_destination_id>/', views.remove_destination_from_trip,
         name='remove_destination_from_trip'),
    path('destination/update-schedule/<int:itinerary_destination_id>/', views.update_destination_schedule,
         name='update_destination_schedule'),

    # Expenses
    path('expense/add/', views.add_expense, name='add_expense'),

    # Profile
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/remove-picture/', views.remove_profile_picture, name='remove_profile_picture'),

    # Static Pages
    path('about/', views.about_view, name='about'),
    path('service/', views.service_view, name='service'),
    path('contact/', views.contact_view, name='contact'),
]

# --- MEDIA FILE CONFIGURATION FOR DEVELOPMENT ONLY ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)