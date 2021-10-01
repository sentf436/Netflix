from django.urls import path
from account.views import (RegistrationView, ActivationView, LoginView, LogoutView,
                           ForgotPasswordView, ForgotPasswordCompleteView, ChangePasswordView)

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='register-account'),
    path('activate/', ActivationView.as_view(), name='acc-activation'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password/complete/', ForgotPasswordCompleteView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
]

