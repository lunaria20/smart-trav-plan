from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=[
        ('resort', 'Resort'),
        ('restaurant', 'Restaurant'),
        ('attraction', 'Attraction'),
        ('beach', 'Beach'),
        ('historical', 'Historical Site')
    ])
    price_range = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class SavedDestination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_destinations')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'destination')
        ordering = ['-saved_at']


class Expense(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=100, choices=[
        ('transport', 'Transportation'),
        ('lodging', 'Lodging'),
        ('food', 'Food & Drinks'),
        ('activity', 'Activities'),
        ('shopping', 'Shopping'),
        ('other', 'Other')
    ])
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

