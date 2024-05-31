from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, reverse_lazy

from .views import logout_view, login_view, get_personal_account_page, \
    add_store, get_my_store, edit_store, get_store_page, \
    delete_store, get_user_data_page, get_personal_account_inactive_adds_page, delete_or_archive_selected_ads, \
    search_of_ads_in_personal_account, register_view_entity, register_view_individual, get_all_dialogs, create_dialog, view_message, \
    delete_dialogs, delete_user_message

app_name = 'users'

urlpatterns = [
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('register_individual/', register_view_individual, name="register_individual"),
    path('register_entity/', register_view_entity, name="register_entity"),
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
    path('personal_account/search_results', search_of_ads_in_personal_account, name="personal_account_search_results"),
    path('personal_account/delete_or_archive_ads/', delete_or_archive_selected_ads, name='delete_or_archive_ads'),
    path('personal_account/archived_adds/', get_personal_account_inactive_adds_page, name='inactive_adds'),
    path('user_data/', get_user_data_page, name='user_data'),
    path('add_store/', add_store, name='add_store'),
    path('my_store/', get_my_store, name='my_store'),
    path('edit_store/<int:store_id>/', edit_store, name='edit_store'),
    path('delete_store/<int:store_id>/', delete_store, name='delete_store'),
    path('store/<slug:slug>/', get_store_page, name='store_page'),
    path('dialogs/', get_all_dialogs, name='dialogs'),
    path('dialogs/create/user:<int:user_id>_and_user:<int:recipient_id>/', create_dialog, name='create_dialog'),
    path('dialogs/<int:chat_id>/', view_message, name='messages'),
    path('dialogs/delete_dialogs/', delete_dialogs, name="delete_dialogs"),
    path('dialogs/<int:chat_id>/delete_user_message/<int:message_id>/', delete_user_message, name="delete_user_message")
]
