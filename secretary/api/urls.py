from django.urls import path

from secretary.api.file_management_views import add_file_view, get_all_files, get_all_archive_files, delete_file, \
    archive_file, unarchive_file
from secretary.api.views import get_secretary_dashboard, add_log_view, get_all_logs_view, \
    delete_log, unarchive_log, archive_log, get_all_archived_log_view, edit_log_view

app_name = 'secretary'

urlpatterns = [
    path('get-secretary-dashboard/', get_secretary_dashboard, name="get_secretary_dashboard"),
    path('add-log/', add_log_view, name="add_log_view"),
    path('edit-log/', edit_log_view, name="edit_log_view"),
    path('get-all-logs/', get_all_logs_view, name="get_all_log_view"),

    path('archive-log/', archive_log, name="archive_log"),
    path('delete-log/', delete_log, name="delete_walkin"),
    path('unarchive-log/', unarchive_log, name="unarchive_walkin"),
    path('get-all-archived-logs/', get_all_archived_log_view, name="get_all_archived_log_view"),

    path('add-file/', add_file_view, name="add_file_view"),
    path('get-all-files/', get_all_files, name="get_all_files_view"),
    path('get-all-archived-files/', get_all_archive_files, name="get_all_archive_files"),
    path('archive-file/', archive_file, name="archive_file"),
    path('unarchive-file/', unarchive_file, name="unarchive_file"),
    path('delete-file/', delete_file, name="delete_file"),

]
