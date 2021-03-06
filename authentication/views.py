from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status, views
from authentication.serializer.auth.serializer import RegisterSerializer, EmailVerificationSerializer
from authentication.serializer.auth.serializer import RequestPasswordResetEmailSerializer
from authentication.serializer.auth.serializer import LoginSerializer, SetNewPasswordSerializer
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from rest_framework import status
from authentication.renderers import UserRenderer
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.serializer.auth.serializer import LogoutSerializer
from authentication.serializer.auth.serializer import UserSerializer, UpdateUserSerializer
from authentication.serializer.pwd.serializer import ChangePasswordSerializer
from rest_framework import permissions
from decouple import config
from django.http import HttpResponsePermanentRedirect
from rest_framework.views import APIView
from expenses.permissions import IsOwner
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import UpdateAPIView

class CustomRedirect(HttpResponsePermanentRedirect):

    # allowed_schemes = [config('APP_SCHEME'), 'http', 'https']
    pass

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
       
        # absurl = 'http://'+current_site+relative_link+"?token="+str(token)
        # absurl = 'http://'+'127.0.0.1:4200/email-verify/'+"?token="+str(token)
        # absurl = 'http://'+'127.0.0.1:4200/email-verify/'+'?token='+str(token) ##local url endpoint
        absurl = 'https://'+'expenseapp-client.herokuapp.com/email-verify/'+'?token='+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer
    def post(self, request):
        data = {'request':request, 'data':request.data}
        serializer = self.serializer_class(data=data)
        email = request.data.get('email',)
        # serializer.is_valid(raise_exception=True)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})

            # redirect_url = request.data.get('redirect_url', '')
            # redirect_url = 'http://localhost:4200/password-reset'; ##local url endpoint

            redirect_url = 'https://expenseapp-client.herokuapp.com/password-reset'; ##production url endpoint
        
            absurl = 'http://'+current_site+relative_link
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            # email_body = 'Hi, \n  Use the link below to Reset your password \n' + absurl
            # email_body = 'Hi, \n  Use the link below to Reset your password \n' + absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your password'}
            Util.send_email(data)
        return Response({'success': 'An email has been sent to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckApiView(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        redirect_url = request.GET.get('redirect_url')
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(config('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(config('FRONTEND_URL', '')+'?token_valid=False')

            # if not PasswordResetTokenGenerator().check_token(user, token):
            #     return Response({'error': 'Token is not valid, please request another one'}, 
            #     status=status.HTTP_401_UNAUTHORIZED
            #     )

            # return Response({'success': True,'message': 'Credentials valid', 'uidb64':uidb64, 'token':token}, 
            # status=status.HTTP_200_OK)


        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            # return Response({'error': 'Token is not valid, please request another one'})


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


class LogoutUser(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        permission_classes = [permissions.IsAuthenticated]
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'message': 'Loggedout successfully'}, status=status.HTTP_200_OK)


class UserApiView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    lookup_id = "pk"


class CurrentUserLoggedInUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordApiView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong Old Password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProfileView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def put(self, request):
        serializer = UpdateUserSerializer(self.request.user, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    