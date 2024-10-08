from django.contrib.auth.models import User
from django.db import models

class friends(models.Model):
    username = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend', on_delete=models.CASCADE)

class Invitation(models.Model):
    sender = models.ForeignKey(User, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_invitations', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

class userprofile(models.Model):
    user = models.ForeignKey(User, related_name='user_id', on_delete=models.CASCADE)
    telephone_number = models.CharField(max_length=20, blank=True, null=True)
