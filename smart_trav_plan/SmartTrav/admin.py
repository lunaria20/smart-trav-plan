from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Destination, Itinerary, ItineraryDestination, SavedDestination, Expense

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'location', 'description')

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