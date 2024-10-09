from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from .models import *
from .serializer import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class NotificationHistoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        notifications = NotificationHistory.objects.filter(created_by=request.user)

        serializer = NotificationHistorySerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        data['created_at'] = timezone.now()

        serializer = NotificationHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
