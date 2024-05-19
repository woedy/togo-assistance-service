from django.urls import path

from clients.api.views import add_client, get_all_clients_view, get_client_details_view, edit_client, archive_client, \
    get_all_archived_clients_view, unarchive_client, delete_client, add_client_complaint

app_name = 'clients'

urlpatterns = [
    path('add-client/', add_client, name="add_client"),
    path('edit-client/', edit_client, name="edit_client"),
    path('get-all-clients/', get_all_clients_view, name="get_all_clients_view"),
    path('get-client-details/', get_client_details_view, name="get_client_details_view"),
    path('archive-client/', archive_client, name="archive_client"),
    path('delete-client/', delete_client, name="delete_client"),
    path('unarchive-client/', unarchive_client, name="unarchive_client"),
    path('get-all-archived-clients/', get_all_archived_clients_view, name="get_all_archived_clients_view"),

    path('add-client-complaint/', add_client_complaint, name="add_client_complaint"),

]
