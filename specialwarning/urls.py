from django.urls import path
from .views import FloodWarningListCreateView, FloodWarningVerifyView

urlpatterns = [
    path('/warnings', FloodWarningListCreateView.as_view(), name='flood-warning-list-create'),
    path('/warnings/<int:pk>/verify', FloodWarningVerifyView.as_view(), name='flood-warning-verify'),
]