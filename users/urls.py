from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from .views import logout_view, LoginAjaxView

urlpatterns = [
    path('logout/', logout_view, name="logout"),
    path('login_ajax/', LoginAjaxView.as_view(), name="login_ajax")



]
