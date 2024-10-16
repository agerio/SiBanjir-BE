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
from datetime import timedelta

class SpecialFloodWarningListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        one_day_ago = now - timedelta(days=1)
        warnings = SpecialFloodWarning.objects.filter(created_at__gte=one_day_ago)

        serializer = SpecialFloodWarningSerializer(warnings, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['created_by'] = request.user.id
        data['created_at'] = timezone.now()

        serializer = SpecialFloodWarningSerializer(data=data, context={'request': request})
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

        if request.user in warning.denied_by.all():
            warning.denied_by.remove(request.user)

        warning.verified_by.add(request.user)
        warning.save()

        return Response({"detail": "Warning verified successfully."}, status=status.HTTP_200_OK)
    

class DenySpecialFloodWarningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        warning = get_object_or_404(SpecialFloodWarning, pk=pk)

        if warning.created_by == request.user:
            return Response({"detail": "You cannot deny your own warning."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in warning.denied_by.all():
            return Response({"detail": "You have already denied this warning."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in warning.verified_by.all():
            warning.verified_by.remove(request.user)

        warning.denied_by.add(request.user)
        warning.save()

        return Response({"detail": "Warning denied successfully."}, status=status.HTTP_200_OK)