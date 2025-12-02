from django.contrib import admin
from django import forms
from .models import Destination, Itinerary, ItineraryDestination, SavedDestination, Expense
from .utils import upload_image_to_supabase


class DestinationAdminForm(forms.ModelForm):
    image_file = forms.ImageField(required=False, help_text="Upload an image (will be stored in Supabase)")

    class Meta:
        model = Destination
        fields = '__all__'


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    form = DestinationAdminForm
    list_display = ('name', 'category', 'location', 'created_at', 'has_image')
    list_filter = ('category',)
    search_fields = ('name', 'location', 'description')

    def has_image(self, obj):
        return bool(obj.image_url)

    has_image.boolean = True
    has_image.short_description = 'Image'

    def save_model(self, request, obj, form, change):
        # Check if a new image was uploaded
        if 'image_file' in request.FILES:
            image_file = request.FILES['image_file']
            # Upload to Supabase and get URL
            image_url = upload_image_to_supabase(image_file, 'images')
            obj.image_url = image_url

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