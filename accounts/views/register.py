import uuid
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models.profile import Profile


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

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

        return redirect('token')
