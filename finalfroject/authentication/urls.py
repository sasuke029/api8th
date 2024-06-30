from django.urls import path
from .views import FarmerRegistrationView,FarmerLoginView,FarmerProfileView,FarmerChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView
urlpatterns = [
    path('register/', FarmerRegistrationView.as_view(), name='register'),
    path('login/', FarmerLoginView.as_view(), name='login'),
    path('profile/', FarmerProfileView.as_view(), name='login'),
    path('changepassword/', FarmerChangePasswordView.as_view(), name='changepaswword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),


]