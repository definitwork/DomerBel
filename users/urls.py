from django.conf import settings
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import profile, login_view

app_name = 'users'
urlpatterns = [
    path('login/', login_view, name="login"),
    # path('register/', register, name='register'),
    path('profile/', profile, name='profile'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='base.html',
        email_template_name='users:password_reset_email',
        success_url=reverse_lazy('users:password_reset_done')
    ),
         name='password_reset'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
