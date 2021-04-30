from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Users should have a username')
        if not email:
            raise ValueError('Users should have an email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise ValueError('Users should have a password')
        user = self.create_user(username, email, password)
        user.is_superuser= True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {
    'twitter': 'twitter',
    'google': 'google',
    'facebook': 'facebook',
    'email': 'email',
}

class User(AbstractBaseUser, PermissionsMixin ):
    email  = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
   
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length = 150, blank=False, null=False, default=AUTH_PROVIDERS.get('email'))
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    

    def get_fullname(self):
        return self.username

    def get_short_username(self):
        return self.username

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }