from django.urls import path

from security_team.api.views.guard_files_views import get_all_archived_guard_files_view, unarchive_guard_file, \
    delete_guard_file, get_all_guard_files_view, archive_guard_file, edit_guard_file_view, add_guard_file_view
from security_team.api.views.guards_views import get_all_guards_view
from security_team.api.views.leave_request_view import add_leave_request, archive_leave_request, change_leave_request_status, delete_leave_request, edit_leave_request, get_all_archived_leave_requests_view, get_all_leave_requests_view, get_leave_request_details_view, unarchive_leave_request
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
    path('delete-guard-file/', delete_guard_file, name="delete_guard_file"),
    path('unarchive-guard-file/', unarchive_guard_file, name="unarchive_guard_file"),
    path('get-all-archived-guard-files/', get_all_archived_guard_files_view, name="get_all_archived_clients_view"),


    path('add-leave-request/', add_leave_request, name="add_leave_request"),
    path('edit-leave-request/', edit_leave_request, name="edit_leave_request"),
    path('change-leave-request-status/', change_leave_request_status, name="change_leave_request_status"),
    path('get-all-leave-requests/', get_all_leave_requests_view, name="get_all_leave_requests_view"),
    path('get-leave-request-details/', get_leave_request_details_view, name="get_leave_request_details_view"),
    path('archive-leave-request/', archive_leave_request, name="archive_leave_request"),
    path('delete-leave-request/', delete_leave_request, name="delete_leave_request"),
    path('unarchive-leave-request/', unarchive_leave_request, name="unarchive_leave_request"),
    path('get-all-archived-leave-requests/', get_all_archived_leave_requests_view, name="get_all_archived_leave_requests_view"),

]
