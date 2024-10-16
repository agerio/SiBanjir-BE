from django.urls import path
from .views import *

urlpatterns = [
    path('', GovAPI.as_view(), name='gov-api'),
    path('refresh', GovAPIRefresh.as_view(), name='refresh-gov-api'),
    path('old', old_govapi.as_view(), name='old-gov-api'),
]