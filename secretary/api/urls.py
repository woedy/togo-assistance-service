from django.urls import path

from secretary.api.views import get_secretary_dashboard, add_walkin_log_view, get_all_walkins_view, archive_walkin, \
    delete_walkin, unarchive_walkin, get_all_archived_walkin_log_view

app_name = 'secretary'

urlpatterns = [
    path('get-secretary-dashboard/', get_secretary_dashboard, name="get_secretary_dashboard"),
    path('add-walkin-logs/', add_walkin_log_view, name="add_walkin_log_view"),
    path('get-all-walkin-logs/', get_all_walkins_view, name="get_all_walkins_view"),

    path('archive-walkin-log/', archive_walkin, name="archive_walkin"),
    path('delete-walkin-log/', delete_walkin, name="delete_walkin"),
    path('unarchive-walkin-log/', unarchive_walkin, name="unarchive_walkin"),
    path('get-all-archived-walkin-logs/', get_all_archived_walkin_log_view, name="get_all_archived_walkin_log_view"),

]
