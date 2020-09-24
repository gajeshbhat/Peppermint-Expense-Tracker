import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email


# User account auth Views

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')


class UserNameValidationView(View):
    def post(self, request):
        user_name_json = json.loads(request.body);
        username = user_name_json['username']  # TODO: Error handling

        # Check username availability
        if str(username).isalnum():
            if User.objects.filter(username=username).exists():
                return JsonResponse({'username_error': 'Sorry! Username already taken!'})
            else:
                return JsonResponse({'username_success': 'Username available'})
        else:
            return JsonResponse({'username_error': 'Invalid Characters for a username. Enter alpha numeric characters'})


class EmailValidationView(View):
    def post(self, request):
        email_name_json = json.loads(request.body);
        email = email_name_json['email']  # TODO: Error handling

        # Check email validity
        if validate_email(str(email)) and not User.objects.filter(email=email).exists():
            return JsonResponse({'email_success': 'Looks good!'})
        else:
            return JsonResponse({'email_error': 'Please enter valid email'})
