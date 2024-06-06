from django.urls import path

from secretary.api.views import get_secretary_dashboard, add_walkin_log_view, get_all_walkins_view, \
    delete_log, unarchive_log, archive_log, get_all_archived_log_view

app_name = 'secretary'

urlpatterns = [
    path('get-secretary-dashboard/', get_secretary_dashboard, name="get_secretary_dashboard"),
    path('add-walkin-logs/', add_walkin_log_view, name="add_walkin_log_view"),
    path('get-all-walkin-logs/', get_all_walkins_view, name="get_all_walkins_view"),

    path('archive-log/', archive_log, name="archive_log"),
    path('delete-log/', delete_log, name="delete_walkin"),
    path('unarchive-log/', unarchive_log, name="unarchive_walkin"),
    path('get-all-archived-logs/', get_all_archived_log_view, name="get_all_archived_log_view"),

]
