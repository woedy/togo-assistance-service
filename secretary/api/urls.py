from django.urls import path

from secretary.api.file_management_views import add_file_view, get_all_files, get_all_archive_files, delete_file, \
    archive_file, unarchive_file
from secretary.api.meeting_views import add_attendees, add_meeting, add_meeting_attendees, add_meeting_reminder, archive_meeting, broadcast_meeting, delete_meeting, edit_meeting, get_all_archived_meetings_view, get_all_meetings_view, get_meeting_details_view, remove_attendees, remove_meeting_attendees, remove_meeting_reminder, set_meeting_complete, set_meeting_ongoing, unarchive_meeting
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


        path('add-meeting/', add_meeting, name="add_meeting"),
    path('edit-meeting/', edit_meeting, name="edit_meeting"),
    path('get-all-meetings/', get_all_meetings_view, name="get_all_meetings_view"),
    path('get-meeting-details/', get_meeting_details_view, name="get_meeting_details_view"),
    path('archive-meeting/', archive_meeting, name="archive_meeting"),
    path('delete-meeting/', delete_meeting, name="delete_meeting"),
    path('unarchive-meeting/', unarchive_meeting, name="unarchive_meeting"),
    path('get-all-archived-meetings/', get_all_archived_meetings_view, name="get_all_archived_meetings_view"),


        path('broadcast-meeting/', broadcast_meeting, name="broadcast_meeting"),
        path('set-meeting-ongoing/', set_meeting_ongoing, name="set_meeting_ongoing"),
        path('set-meeting-complete/', set_meeting_complete, name="set_meeting_complete"),


        path('add-attendees/', add_attendees, name="add_attendees"),
        path('remove-attendee/', remove_attendees, name="remove_attendees"),

        path('add-meeting-attendees/', add_meeting_attendees, name="add_meeting_attendees"),
        path('remove-meeting-attendee/', remove_meeting_attendees, name="remove_meeting_attendees"),


        path('add-meeting-reminder/', add_meeting_reminder, name="add_meeting_reminder"),
        path('remove-meeting-reminder/', remove_meeting_reminder, name="remove_meeting_reminder"),
]
