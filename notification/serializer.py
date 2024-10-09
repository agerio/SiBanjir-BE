from rest_framework import serializers
from .models import NotificationHistory

class NotificationHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NotificationHistory
        fields = ['name', 'created_at', 'created_by']