from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation

from authentication.models import User
from rest_framework.response import Response
from rest_framework import status

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
  
# class UpdateUserSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField()
