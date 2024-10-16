from django.urls import path
from .views import *

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user-register'),
    path('login', UserLoginView.as_view(), name='user-login'), 
    path('me', UserInformation.as_view(), name='user-authentication'),
    path('adwokacik', SomeProtectedView.as_view(), name='user-authentication'),
    path('sendInvitation', SendInvitationView.as_view(), name='send-invitation'),
    path('listInvitation', listInvitationView.as_view(), name='list-invitation'),
    path('createFriend', createFriend.as_view(), name='create-friend'),
    path('deleteInvitation', DeleteInvitationView.as_view(), name='delete-invitation'),  # New endpoint for deleting invitations
    path('profile/update/telephoneNumber', updateTelephone.as_view(), name='telephone-update'),
    path('profile/update/picture', updateUserImage.as_view(), name='picture-update'),
    path('profile/update/username', updateUsername.as_view(), name='username-update'),
    path('profile/update/password', updatePassword.as_view(), name='password-update'),
    path('searchFriend', UserInformation.as_view(), name='search-user'),
    path('listFriend', ListFriend.as_view(), name='list-friend'),
    path('sendLocation',UserLocation.as_view(),name='send-location'),
    path('switchLocation',switchLocation.as_view(),name='switch-location')
]
