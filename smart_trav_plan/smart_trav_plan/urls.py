from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

admin.site.site_header = "SmartTrav Administration"
admin.site.site_title = "SmartTrav Admin"
admin.site.index_title = "Welcome to SmartTrav Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/login/', permanent=False)),  # ✅ Redirect root to login
    path('', include('SmartTrav.urls')),
]