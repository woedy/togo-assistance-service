from django.urls import path

from security_team.api.views.guard_files_views import get_all_archived_guard_files_view, unarchive_guard_file, \
    delete_guard_file, get_all_guard_files_view, archive_guard_file, edit_guard_file_view, add_guard_file_view
from security_team.api.views.guards_views import get_all_guards_view
from security_team.api.views.slot_views import set_guard_availability, list_guard_availability

app_name = 'security_team'

urlpatterns = [
    path('set-guard-availability/', set_guard_availability, name="set_guard_availability"),
    path('list-guard-availability/', list_guard_availability, name="list_guard_availability"),
    path('get-all-guards/', get_all_guards_view, name="get_all_guards_view"),

    path('add-guard-file/', add_guard_file_view, name="add_guard_file_view"),
    path('edit-guard-file/', edit_guard_file_view, name="edit_guard_file_view"),
    path('get-all-guard-files/', get_all_guard_files_view, name="get_all_guard_files_view"),
    path('archive-guard-file/', archive_guard_file, name="archive_guard_files"),
    path('delete-guard-file/', delete_guard_file, name="delete_client"),
    path('unarchive-guard-file/', unarchive_guard_file, name="unarchive_client"),
    path('get-all-archived-guard-files/', get_all_archived_guard_files_view, name="get_all_archived_clients_view"),

]
