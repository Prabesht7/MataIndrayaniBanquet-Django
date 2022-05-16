from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required


class Contact(View):
    login_required(login_url='Login')

    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        pass
