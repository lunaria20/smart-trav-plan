from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('smart_trav_plan.accounts.urls')),
    path('', include('smart_trav_plan.SmartTrav.urls')),  # root app
]
