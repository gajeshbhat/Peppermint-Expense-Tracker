from django.urls import path
from .views import RegistrationView, UserNameValidationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', RegistrationView.as_view(), name="register_new_user"),
    path('validate_username', csrf_exempt(UserNameValidationView.as_view()), name="validate_username"),
]