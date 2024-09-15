from django.urls import path
from .views import *

urlpatterns = [
    path('/register', UserRegistrationView.as_view(), name='user-register'),
    path('/login', UserLoginView.as_view(), name='user-login'), 
    path('/me', UserInformation.as_view(), name='user-authentication'),
    path('/adwokacik', SomeProtectedView.as_view(), name='user-authentication'),
    path('/sendInvitation', SendInvitationView.as_view(), name='send-invitation'),
    path('/listInvitation', listInvitationView.as_view(), name='list-invitation'),
    path('/createFriend', createFriend.as_view(), name='create-friend')      
]
