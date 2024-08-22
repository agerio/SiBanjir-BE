from rest_framework import serializers
from .models import *

class HelloWorldSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelloWorld
        fields = ['text']