from django.urls import path
from .views.login import Login
from .views.register import Register, verify, error_page
from .views.token import TokenSend
from .views.success import Success
from .views.forgetpassword import ForgetPassword, ChangePassword

urlpatterns = [
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('token', TokenSend.as_view(), name='token_send'),
    path('success', Success.as_view(), name='success'),
    path('verify/<auth_token>', verify, name="verify"),
    path('error', error_page, name="error"),
    path('change_password/<token>', ChangePassword, name='change_password'),
    path('forget_password', ForgetPassword.as_view(), name='forget_password'),
]
