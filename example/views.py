from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import *
from . serializer import *

# Create your views here.
class ExampleView(APIView):
    serializer_class = HelloWorldSerializer

    def get(self, request):
        output = HelloWorld.objects.all().first().text
        return Response(output)