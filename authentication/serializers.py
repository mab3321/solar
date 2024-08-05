from rest_framework import serializers
from authentication.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.utils import Util
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
import re
import os


User = get_user_model()

class SendSignupLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validates the email address and checks if it already exists in the database.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"message": "Email already exists.", 'status_code': '400'})
        return value

    def create(self, validated_data):
        """
        Generates and sends the signup link email.
        """
        email = validated_data['email']
        print(validated_data['email'])
        email_encoded = urlsafe_base64_encode(email.encode())

        signup_link = f'http://localhost:8000/api/user/register/{email_encoded}'

        subject = 'Bizaibo Registration'
        template_path = 'EMAIL/registration_email.html'
        context = {'signup_link': signup_link,'email': email}

        # Send email
        Util.send_email(subject, template_path, context, email)

        return validated_data
    
class UserRegistrationSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields=['username','email', 'password']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'confirm_password']

  def validate(self, attrs):
    password = attrs.get('password')
    confirm_password = attrs.get('confirm_password')
    user = self.context.get('user')
    if password != confirm_password:
      raise serializers.ValidationError({"message":"Password and Confirm Password doesn't match", "status_code": "400"})
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    url = serializers.URLField() 

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        url = attrs.get('url')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"{url}{uid}/{token}/"

            # Send Email
            subject = 'Reset Your Password'
            template_path = 'EMAIL/password_reset_email.html'
            context = {'reset_link': reset_link}

            Util.send_email(subject, template_path, context,email)
            return attrs
        else:
            raise serializers.ValidationError({"message": 'You are not a Registered User', "status_code": "400"})

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  confirm_password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'confirm_password']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      confirm_password = attrs.get('confirm_password')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != confirm_password:
        raise serializers.ValidationError({"message":"Password and Confirm Password doesn't match", "status_code": "400"})
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError({"message":'Token is not Valid or Expired', "status_code": "401"})
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError({"message":'Token is not Valid or Expired', "error_code": "401"})