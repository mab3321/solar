from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from authentication.serializers import SendSignupLinkSerializer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate, logout
from authentication.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_decode
import base64
from rest_framework.authtoken.models import Token
from django.shortcuts import render

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SendSignupLinkView(APIView):
    renderer_classes = [UserRenderer]  # Use the UserRenderer for responses

    def post(self, request, format=None):
        serializer = SendSignupLinkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will trigger the email sending logic in the serializer
            return Response({'message': 'Signup link sent to your email', 'status_code': '200'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def is_valid_base64_encoded_email(self, encoded_email):
        try:
            decoded_bytes = base64.urlsafe_b64decode(encoded_email.encode())
            decoded_email = decoded_bytes.decode()
            return '@' in decoded_email  # Basic check if decoded string contains '@'
        except (TypeError, UnicodeDecodeError, base64.binascii.Error):
            return False

    def post(self, request, encoded_email, format=None):
        try:
            email = urlsafe_base64_decode(encoded_email).decode()
        except UnicodeDecodeError:
            raise Http404({"message":"Invalid encoded email", 'status_code': '400'})

        request.data['email'] = email
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)  # Assuming you have a method to generate tokens
            return Response({'token': token, 'message': 'Registration Successful','status_code': '201'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'Login Success', 'status_code': '200'}, status=status.HTTP_200_OK)
        return Response({'message':'Email or Password is not Valid', 'status_code': '401'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response({'status': 'sucess','data':serializer.data, 'status_code': '200'}, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Changed Successfully', 'status_code': '200'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Reset link send. Please check your Email', 'status_code': '200'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password Reset Successfully', 'status_code': '200'}, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response({'message': 'Logout Successful', 'status_code': '200'}, status=status.HTTP_200_OK)

def home(request):
    return  render(request,'OTHER/home.html')
 

