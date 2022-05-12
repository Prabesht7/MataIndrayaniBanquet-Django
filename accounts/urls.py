from django.urls import path
from .views.login import Login
from .views.register import Register
from .views.token import TokenSend
from .views.success import Success

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('token', TokenSend.as_view(), name='token_send'),
    path('success', Success.as_view(), name='success')
]
