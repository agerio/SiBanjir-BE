from rest_framework import serializers
from .models import SpecialFloodWarning

class SpecialFloodWarningSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = SpecialFloodWarning
        fields = '__all__'

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_profile_picture(self, obj):
        profile = getattr(obj.created_by, 'profile', None)
        if profile and profile.profile_picture:
            return profile.profile_picture.url
        return None