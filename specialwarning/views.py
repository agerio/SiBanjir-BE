from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from .models import FloodWarning
from .serializer import *

# List and Create Flood Warnings
class FloodWarningListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        warnings = FloodWarning.objects.all()

        print(request.data)
        serializer = FloodWarningDeserializer(warnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # print(request.data)

        serializer = FloodWarningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

# Verify a Flood Warning
class FloodWarningVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            flood_warning = FloodWarning.objects.get(pk=pk, is_verified=False)
        except FloodWarning.DoesNotExist:
            return Response({"error": "Flood warning not found or already verified"}, status=status.HTTP_404_NOT_FOUND)

        # Verification logic
        flood_warning.is_verified = True
        flood_warning.verified_by = request.user
        flood_warning.verified_at = timezone.now()
        flood_warning.save()

        serializer = VerifyFloodWarningSerializer(flood_warning)
        return Response(serializer.data, status=status.HTTP_200_OK)
