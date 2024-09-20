from django.urls import path
from .views import *

urlpatterns = [
    path('', govapi.as_view(), name='gov-api'),   
]