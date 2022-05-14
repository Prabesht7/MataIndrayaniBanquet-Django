from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models.profile import Profile
from django.contrib.auth import authenticate, login


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'User is no Found')
            return redirect('login')

        profile_obj = Profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not Verified')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Invalid Username or Password')
            return redirect('login')
        login(request, user)
        return redirect('register')
