from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from .models import *
from .serializer import *
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# List and Create Flood Warnings
class SpecialFloodWarningListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        warnings = SpecialFloodWarning.objects.all()

        print(request.data)
        serializer = SpecialFloodWarningDeserializer(warnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Create a mutable copy of the request data to modify it
        data = request.data.copy()

        # Automatically set the created_by and created_at fields
        data['created_by'] = request.user.id  # Set the creator as the current user
        data['created_at'] = timezone.now()   # Automatically set the current timestamp
        
        # Explicitly set 'verified_by' as an empty list or null equivalent
        # data['verified_by'] = []  # Setting it to an empty list as a placeholder
        print(data)
        # Use the FloodWarningSerializer to validate and save
        serializer = SpecialFloodWarningSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class VerifySpecialFloodWarningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Fetch the flood warning by its ID
        warning = get_object_or_404(SpecialFloodWarning, pk=pk)

        # Check if the logged-in user is not the creator
        if warning.created_by == request.user:
            return Response({"detail": "You cannot verify your own warning."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has already verified this warning
        if request.user in warning.verified_by.all():
            return Response({"detail": "You have already verified this warning."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the verified_by field and save
        warning.verified_by.add(request.user)
        warning.save()

        return Response({"detail": "Warning verified successfully."}, status=status.HTTP_200_OK)