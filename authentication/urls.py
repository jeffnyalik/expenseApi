from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view, name='logout'),
    path('user/', views.CurrentUserLoggedInUserView.as_view(), name='current_user'),
    path('users/', views.UserApiView.as_view(), name='users'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('update-profile/', views.UpdateProfileView.as_view(), name='update-profile'),
    path('change-user-password/', views.ChangePasswordApiView.as_view(), name='change-user-password'),
    path('email-verify', views.VerifyEmail.as_view(), name='email-verify'),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/', views.PasswordTokenCheckApiView.as_view(), name='password-reset-confirm'),
    path('password-change/', views.SetNewPasswordAPIView.as_view(), name='password-change'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]