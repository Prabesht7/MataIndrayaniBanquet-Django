from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from accounts.models.profile import Profile
from django.conf import settings
import uuid


class ForgetPassword(View):
    def get(self, request):
        return render(request, 'forget_password.html')

    def post(self, request):
        try:
            if request.method == 'POST':
                username = request.POST.get('username')

                if not User.objects.filter(username=username).first():
                    messages.success(request, 'Not user found with this username.')
                    return redirect('forget_password')

                user_obj = User.objects.get(username=username)
                token = str(uuid.uuid4())
                profile_obj = Profile.objects.get(user=user_obj)
                profile_obj.forget_password_token = token
                profile_obj.save()
                send_forget_password_mail(user_obj.email, token)
                messages.success(request, 'An email is sent.')
                return redirect('forget_password')

        except Exception as e:
            print(e)
        return render(request, 'forget_password.html')


def ChangePassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change_password/{token}')

            if new_password != confirm_password:
                messages.success(request, 'Both password should be same')
                return redirect(f'/change_password/{token}')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request, 'change_password.html', context)


def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
