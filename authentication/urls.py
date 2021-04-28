from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('email-verify/', views.VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckApiView.as_view(), name='password-reset-confirm'),
    path('password-change/', views.SetNewPasswordAPIView.as_view(), name='password-change'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]