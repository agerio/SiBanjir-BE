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

class SpecialFloodWarningListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        warnings = SpecialFloodWarning.objects.all()

        serializer = SpecialFloodWarningSerializer(warnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['created_by'] = request.user.id
        data['created_at'] = timezone.now()

        serializer = SpecialFloodWarningSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class VerifySpecialFloodWarningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        warning = get_object_or_404(SpecialFloodWarning, pk=pk)

        if warning.created_by == request.user:
            return Response({"detail": "You cannot verify your own warning."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in warning.verified_by.all():
            return Response({"detail": "You have already verified this warning."}, status=status.HTTP_400_BAD_REQUEST)

        warning.verified_by.add(request.user)
        warning.save()

        return Response({"detail": "Warning verified successfully."}, status=status.HTTP_200_OK)
    

class DenySpecialFloodWarningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        warning = get_object_or_404(SpecialFloodWarning, pk=pk)

        if warning.created_by == request.user:
            return Response({"detail": "You cannot deny your own warning."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in warning.verified_by.all():
            return Response({"detail": "You have already denied this warning."}, status=status.HTTP_400_BAD_REQUEST)

        warning.denied_by.add(request.user)
        warning.save()

        return Response({"detail": "Warning denied successfully."}, status=status.HTTP_200_OK)