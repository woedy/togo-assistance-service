from django.urls import path

from clients.api.views import add_client, get_all_clients_view, get_client_details_view, edit_client, archive_client, \
    get_all_archived_clients_view, unarchive_client, delete_client
from secretary.api.views import get_secretary_dashboard

app_name = 'client'

urlpatterns = [
    path('get-secretary-dashboard/', get_secretary_dashboard, name="get_secretary_dashboard"),
]
