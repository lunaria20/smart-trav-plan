from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)  # ✅ fixed path

    def __str__(self):
        return self.name
