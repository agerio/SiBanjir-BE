from django.contrib.auth.models import User
from user.models import *
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Username and password are required.")
        
        attrs['user'] = user
        return attrs

class SendInvitationSerializer(serializers.Serializer):
    recipient_username = serializers.CharField(required=True)
    

    def validate(self, attrs):
        if not User.objects.filter(username=attrs['recipient_username']).exists():
            raise serializers.ValidationError("Recipient does not exist.")
        return attrs

class listInvitationSerializer(serializers.Serializer):
    sender = serializers.CharField(source='sender.username')
    class Meta:
        model = Invitation
        fields = ["sender"]

class createFriendsSerializer(serializers.Serializer):
    sender = serializers.CharField(required=True)

    def validate(self, attrs):
        if not User.objects.filter(username=attrs['sender']).exists():
            raise serializers.ValidationError("sender does not exist.")
        return attrs