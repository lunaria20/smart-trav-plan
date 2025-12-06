from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    image_url = models.URLField(max_length=500, blank=True, null=True)
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


class ItineraryDestination(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='itinerary_destinations')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    visit_date = models.DateField(null=True, blank=True)  # NEW FIELD
    visit_time = models.TimeField(null=True, blank=True)  # NEW FIELD
    added_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('itinerary', 'destination')
        ordering = ['visit_date', 'visit_time', 'added_at']  # UPDATED ORDERING

    def __str__(self):
        return f"{self.destination.name} in {self.itinerary.title}"


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Auto-create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()