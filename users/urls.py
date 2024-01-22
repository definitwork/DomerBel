from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from .views import login_view, registration, logout_view, send_email, PasswordResetView

app_name = 'users'
urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', registration, name='register'),
    path('logout/', logout_view, name="logout"),
    path('send_email', send_email, name='send_email'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="base.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'),

    path('reset_password_sent/',
         PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")
         ),
         name='password_reset_confirm'),

    path('reset_password_complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]
