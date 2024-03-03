from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy
from .views import logout_view, login_view, register_view, get_personal_account_page, get_incoming_page, \
    get_outgoing_page, get_sent_page, get_admin_message_page, add_store, get_my_store, edit_store, get_store_page, \
    delete_store

app_name = 'users'
urlpatterns = [
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="base.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")),
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

    path('personal_account/', get_personal_account_page, name='personal_account'),
    path('incoming_messages/', get_incoming_page, name='incoming_messages'),
    path('outgoing_messages/', get_outgoing_page, name='outgoing_messages'),
    path('sent_messages/', get_sent_page, name='sent_messages'),
    path('admin_messages/', get_admin_message_page, name='admin_messages'),
    path('add_store/', add_store, name='add_store'),
    path('my_store/', get_my_store, name='my_store'),
    path('edit_store/<int:store_id>/', edit_store, name='edit_store'),
    path('delete_store/<int:store_id>/', delete_store, name='delete_store'),
    path('store/<slug:slug>/', get_store_page, name='store_page'),
]
