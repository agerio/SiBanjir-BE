from rest_framework import serializers
from .models import SpecialFloodWarning

class SpecialFloodWarningDeserializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialFloodWarning
        fields = ['name', 'long','lat', 'created_by', 'verified_by', 'flood_image']
        read_only_fields = ['created_by', 'verified_by']

    def get_latlong(self, obj):
        return f"{obj.latitude}, {obj.longitude}"
    
class SpecialFloodWarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialFloodWarning
        fields = '__all__'
