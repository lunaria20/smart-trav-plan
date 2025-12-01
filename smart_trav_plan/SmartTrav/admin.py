from django.contrib import admin
from .models import Destination, Itinerary, ItineraryDestination, SavedDestination, Expense
from .utils import upload_image_to_supabase  # Import the utility


# Register your models here.
from django.contrib import admin
from .models import Destination, Itinerary, ItineraryDestination, SavedDestination, Expense

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'location', 'description')

    def save_model(self, request, obj, form, change):
        """Override save to upload image to Supabase"""
        # Check if a new image was uploaded
        if 'image' in form.changed_data and obj.image:
            # Upload to Supabase and get URL
            image_url = upload_image_to_supabase(obj.image, 'destinations')
            # Store the URL instead of the file
            obj.image = image_url

        super().save_model(request, obj, form, change)

@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'start_date', 'end_date', 'budget', 'created_at')
    list_filter = ('user', 'start_date')
    search_fields = ('title', 'notes')

@admin.register(ItineraryDestination)
class ItineraryDestinationAdmin(admin.ModelAdmin):
    list_display = ('itinerary', 'destination', 'added_at')
    list_filter = ('added_at',)

@admin.register(SavedDestination)
class SavedDestinationAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'saved_at')
    list_filter = ('user',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'itinerary', 'category', 'amount', 'date')
    list_filter = ('category', 'date')
    search_fields = ('description',)