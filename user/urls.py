from django.urls import path
from .views import UserRegistrationView
from .views import UserLoginView
from .views import SomeProtectedView

urlpatterns = [
    path('/register', UserRegistrationView.as_view(), name='user-register'),
    path('/login', UserLoginView.as_view(), name='user-login'), 
    path('/adwokacik', SomeProtectedView.as_view(), name='user-authentication') 
]
