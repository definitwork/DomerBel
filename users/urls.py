from django.urls import path
from .views import logout_view, login_view, register_view, reset_person_password

app_name = 'users'
urlpatterns = [
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('change_password/', reset_person_password, name="change_password")



]
