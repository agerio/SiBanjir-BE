from rest_framework import serializers
from .models import SpecialFloodWarning

class SpecialFloodWarningSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpecialFloodWarning
        fields = '__all__'

    def get_latlong(self, obj):
        return f"{obj.latitude}, {obj.longitude}"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.image:
            representation['image'] = instance.image.url
        else:
            representation['image'] = None

        return representation