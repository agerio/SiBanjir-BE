from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class friends(models.Model):
    username = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)

class Invitation(models.Model):
    sender = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_invitations', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = CloudinaryField('image', null=True, blank=True)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
    long = models.DecimalField(max_digits=35, decimal_places=23,null=True)
    lat = models.DecimalField(max_digits=35, decimal_places=23,null=True)
    allow_location = models.BooleanField(default=False)
    
