from django.shortcuts import render, redirect
from django.views import View


class TokenSend(View):
    def get(self, request):
        return render(request, 'token_send.html')
