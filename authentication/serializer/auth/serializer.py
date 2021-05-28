from rest_framework import serializers
from authentication.models import User
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from authentication.utils import Util
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=6, write_only=True)

    class Meta:
        model=User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        if not username.isalnum():
            raise serializers.ValidationError('Username should only contain alphanumeric character')
        if len(username) < 6:
            raise serializers.ValidationError('Username should be atleast 6 characters')
        if password == 'admin12' or password == 'admin123' or password == 'password' or password == 'password12':
            raise serializers.ValidationError('Password is too common')
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=600)
    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=68, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'access':user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }


    class Meta:
        model = User
        fields  = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Email or Password, try again')
        if not user.is_active:
            raise AuthenticationFailed('User is disabled, Confirm with the Adminstrator')
        if not user.is_verified:
            raise AuthenticationFailed('User has not been verified')
       
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }

        

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=3)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']



class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email', 
            'first_name', 
            'last_name',
            'city',
            'phone_number', 
            'is_active'
            ]



class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    # username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username', 
            'first_name', 
            'last_name',
            'phone_number',
            'city'
        ]

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'phone_number': {'required': True},
            'city': {'required': True}
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.phone_number = validated_data['phone_number']
        instance.city = validated_data['city']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()
        return instance