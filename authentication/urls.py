from django.urls import path
from .views import RegistrationView, UserNameValidationView,EmailValidationView, LoginView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register_new_user"),
    path('login', RegistrationView.as_view(), name="user_login"),
    path('validate_username', csrf_exempt(UserNameValidationView.as_view()), name="validate_username"),
    path('validate_email', csrf_exempt(EmailValidationView.as_view()), name="validate_email"),
]