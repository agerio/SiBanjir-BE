from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class SpecialFloodWarning(models.Model):
    name = models.CharField(max_length=255)
    long = models.DecimalField(max_digits=19, decimal_places=5)
    lat = models.DecimalField(max_digits=19, decimal_places=5)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    verified_by = models.ManyToManyField(User, null=True, blank=True)
    image = CloudinaryField('image', null=True, blank=True)