import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate


# User account auth Views

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Please Enter Password more than 6 Characters')
        else:
            new_user = User.objects.create_user(username=username, email=email, password=password)
            new_user.save()
            self.send_confirmation_email(email)
            messages.add_message(request, messages.SUCCESS, 'Registration Successful! Please check your email!')
        return render(request, 'authentication/register.html')

    def send_confirmation_email(self, email):
        send_mail(
            'Peppermint Registration',
            'Your Registration was successful!',
            'noreply@pepperminttracker.com',
            [str(email)],
            fail_silently=False,
        )


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


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if authenticate(request,username=username,password=password) is not None:
            messages.add_message(request, messages.SUCCESS, "Login Successful!")
            return render(request, 'authentication/login.html') # TODO Redirect to Dashboard page
        else:
            messages.add_message(request, messages.ERROR, "Invalid credentials!")
            return render(request, 'authentication/login.html')
