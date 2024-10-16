from rest_framework import serializers
from .models import *

class FloodWatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = FloodWatch
        fields = '__all__'