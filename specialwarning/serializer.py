from rest_framework import serializers
from .models import SpecialFloodWarning

class SpecialFloodWarningSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    has_verified = serializers.SerializerMethodField()
    has_denied = serializers.SerializerMethodField()
    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = SpecialFloodWarning
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = instance.created_by.username

        if instance.image:
            representation['image'] = instance.image.url
        else:
            representation['image'] = None

        return representation

    def get_profile_picture(self, obj):
        profile = getattr(obj.created_by, 'profile', None)
        if profile and profile.profile_picture:
            return profile.profile_picture.url
        return None
    
    def get_has_verified(self, obj):
        request_user = self.context['request'].user
        return obj.verified_by.filter(id=request_user.id).exists()

    def get_has_denied(self, obj):
        request_user = self.context['request'].user
        return obj.denied_by.filter(id=request_user.id).exists()
    
    def get_is_creator(self, obj):
        request_user = self.context['request'].user
        return obj.created_by == request_user