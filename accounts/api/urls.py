from django.urls import path

from accounts.api.user_files_views import add_user_file, get_all_user_files_view, get_user_file_details_view, \
    archive_user_file, delete_user_file, unarchive_user_file, get_all_archived_user_files_view
from accounts.api.views import register_user, verify_user_email, resend_email_verification, UserLogin, \
    PasswordResetView, confirm_otp_password_view, resend_password_otp, new_password_reset_view, remove_user_view, \
    edit_profile, list_all_users_view, get_user_details_view, archive_user_view, unarchive_user_view, \
    list_all_archived_users_view, delete_user_view

app_name = 'accounts'

urlpatterns = [
    #path('register-user/', register_user, name="register_user"),


    path('register-user/', register_user, name="register_user"),
    path('edit-profile/', edit_profile, name="edit_profile"),

    path('verify-user-email/', verify_user_email, name="verify_user_email"),
    path('resend-email-verification/', resend_email_verification, name="resend_email_verification"),
    path('login-user/', UserLogin.as_view(), name="login_user"),

    path('forgot-user-password/', PasswordResetView.as_view(), name="forgot_password"),
    path('confirm-password-otp/', confirm_otp_password_view, name="confirm_otp_password"),
    path('resend-password-otp/', resend_password_otp, name="resend_password_otp"),
    path('new-password-reset/', new_password_reset_view, name="new_password_reset_view"),

    path('remove_user/', remove_user_view, name="remove_user_view"),


    path('get-all-users/', list_all_users_view, name="list_all_users_view"),
    path('get-all-archived-users/', list_all_archived_users_view, name="list_all_archived_users_view"),
    path('get-user-details/', get_user_details_view, name="get_user_details_view"),
    path('archive-user/', archive_user_view, name="archive_user_view"),
    path('unarchive-user/', unarchive_user_view, name="unarchive_user_view"),
    path('delete-user/', delete_user_view, name="delete_user_view"),

    path('add-user-file/', add_user_file, name="add_client"),
    path('get-all-user-files/', get_all_user_files_view, name="get_all_user_files_view"),
    path('get-user-file-details/', get_user_file_details_view, name="get_user_file_details_view"),
    path('archive-user-file/', archive_user_file, name="archive_user_file"),
    path('delete-user-file/', delete_user_file, name="delete_user_file"),
    path('unarchive-user-file/', unarchive_user_file, name="unarchive_user_file"),
    path('get-all-archived-user-files/', get_all_archived_user_files_view, name="get_all_archived_user_files_view"),

]
