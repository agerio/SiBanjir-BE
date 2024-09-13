from rest_framework import serializers
from .models import FloodWarning

class FloodWarningDeserializer(serializers.ModelSerializer):
    latlong = serializers.SerializerMethodField()

    class Meta:
        model = FloodWarning
        fields = ['id', 'location_name','latlong', 'description', 'is_verified',]
        read_only_fields = ['is_verified']

    def get_latlong(self, obj):
        return f"{obj.latitude}, {obj.longitude}"
    
class FloodWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloodWarning
        fields = '__all__'

class VerifyFloodWarningSerializer(serializers.ModelSerializer):
    latlong = serializers.SerializerMethodField()

    class Meta:
        model = FloodWarning
        fields = ['is_verified', 'verified_by', 'verified_at', 'latlong']
        read_only_fields = ['verified_by', 'verified_at', 'latlong']

    def get_latlong(self, obj):
        return f"{obj.latitude}, {obj.longitude}"
