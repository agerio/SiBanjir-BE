from django.urls import path
from .views import *

urlpatterns = [
    path('/warnings', SpecialFloodWarningListCreateView.as_view(), name='flood-warning-list-create'),
    path('/warnings/<int:pk>/verify', VerifySpecialFloodWarningView.as_view(), name='flood-warning-verify'),
]