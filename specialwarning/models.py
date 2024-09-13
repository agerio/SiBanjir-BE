from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FloodWarning(models.Model):
    location_name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_warnings")
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.location_name

    def verify(self, user):
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.save()