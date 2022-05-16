from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class Homepage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'homepage.html')

    def post(self, request):
        pass
