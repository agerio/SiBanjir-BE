from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth.models import User
from user.models import Invitation, friends
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({"message": "User created successfully", "token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self ,request):
        return Response("hello world")
    
class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)  # Log in the user and create a session
            token, created = Token.objects.get_or_create(user=user) 
            return Response({'message': 'Login successful', 'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserInformation(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserInformationDeserializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)

        if 'profile_picture' in request.data:
            profile_picture = request.data['profile_picture']
            user_profile.profile_picture = profile_picture
            user_profile.save()

            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Profile picture not provided."}, status=status.HTTP_400_BAD_REQUEST)

class SomeProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"message": "This is a protected view!"})
    
class SendInvitationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = SendInvitationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            recipient = User.objects.get(username=serializer.validated_data['recipient_username'])
            Invitation.objects.create(
                sender=request.user,
                recipient=recipient,
            )
            return Response({"message": "Invitation sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class listInvitationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        invitation = Invitation.objects.filter(recipient=user)
        serializer = listInvitationSerializer(invitation, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class createFriend(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = createFriendsSerializer(data=request.data)
        if serializer.is_valid():
            sender = User.objects.get(username=serializer.validated_data['sender'])
            friends.objects.create(
                username=request.user,
                friend=sender
            )
            return Response({"message": "Friend added successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteInvitationView(APIView):  # New view for deleting invitations
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, *args, **kwargs):
        sender_username = request.data.get('sender_username')
        recipient_username = request.data.get('recipient_username')

        try:
            sender = User.objects.get(username=sender_username)
            recipient = User.objects.get(username=recipient_username)
            invitation = Invitation.objects.get(sender=sender, recipient=recipient)
            invitation.delete()
            return Response({"message": "Invitation deleted successfully"}, status=status.HTTP_200_OK)
        except Invitation.DoesNotExist:
            return Response({"error": "Invitation not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "Sender or recipient not found"}, status=status.HTTP_404_NOT_FOUND)