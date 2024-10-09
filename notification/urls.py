from django.urls import path
from .views import *

urlpatterns = [
    path('history', NotificationHistoryListCreateView.as_view(), name='notification-history-list-create')
]