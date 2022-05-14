import uuid
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models.profile import Profile
from django.conf import settings
from django.core.mail import send_mail


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password, first_name, last_name)

        try:
            if User.objects.filter(username=username).first():
                messages.success(request, 'Username is already registered')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is already registered')
                return redirect('register')

            user_obj = User.objects.create(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)

        except Exception as e:
            print(e)
        return render(request, 'token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "Your account is already verified")
                return render('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, "Your account have been verified")
            return redirect("login")
        else:
            return redirect("error")
    except Exception as e:
        print(e)


def error_page(request):
    return render(request, 'error.html')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
