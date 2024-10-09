from django.db import models
from django.contrib.auth.models import User

class NotificationHistory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_by', on_delete=models.CASCADE)