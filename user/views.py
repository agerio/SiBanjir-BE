from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.utils import timezone
from django.contrib.auth.models import User 
from user.models import Invitation, friends, UserProfile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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
    
    def post(self, request, *args, **kwargs):
        serializer = SendInvitationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            recipient = User.objects.get(username=serializer.validated_data['recipient_username'])
            serializer = UserInformationDeserializer(recipient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateUserImage(APIView):
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

class FindUserByUsername(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        username = request.query_params.get('username', '')
        if not username:
            return Response({"error": "Please provide a username"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
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
        
class  updateTelephone(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def patch(self, request, *args, **kwargs):
        user = request.user  
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = None

        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            if user_profile:
                user_profile.telephone_number = serializer.validated_data['telephone_number']
                user_profile.save()
            else:
                UserProfile.objects.create(
                    telephone_number=serializer.validated_data['telephone_number'],
                    user=request.user,
                )
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class updateUsername(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = usernameUpdateSerializer(data = request.data)
        if serializer.is_valid():
            user.username = serializer.validated_data['username']
            user.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class updatePassword(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = passwordUpdateSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListFriend(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        friend_instances = friends.objects.filter(username=request.user)
        serializer = FriendSerializer(friend_instances,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLocation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self,request, *args, **kwargs):
        user = request.user
        serializer = getLocationSerializer(data=request.data)
        if request.user.profile.allow_location == True:
            if serializer.is_valid():
                user.profile.lat = serializer.validated_data['lat']
                user.profile.save()
                user.profile.long = serializer.validated_data['long']
                user.profile.save()

                user.last_login = timezone.now()
                user.save()
                return Response({"message": "location updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "location turned off."}, status=status.HTTP_200_OK)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request, *args, **kwargs):
        friend_instances = friends.objects.filter(username=request.user)
        serializer = UserLocationSerializer(friend_instances,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class switchLocation(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self,request, *args, **kwargs):
        profile = request.user.profile
        serializer = UserLocationStatusSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        profile = request.user.profile
        location_status = profile.allow_location
        if location_status == False:
            profile.allow_location = True
            profile.save()
        else:
            profile.allow_location = False
            profile.lat = None
            profile.long = None
            profile.save()
        return Response({"message": "location switched successfully."}, status=status.HTTP_200_OK)
