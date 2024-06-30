from django.urls import path

from legal.api.views import add_client_request_contract_view, get_all_client_contracts, archive_contract, \
    unarchive_contract, delete_contract

app_name = 'legal'

urlpatterns = [
    path('add-booking-contract/', add_client_request_contract_view, name="send_estimate_to_client"),
    path('get-all-client-contracts/', get_all_client_contracts, name="get_all_client_contracts"),
    path('archive-client-contract/', archive_contract, name="archive_contract"),
    path('unarchive-client-contract/', unarchive_contract, name="unarchive_contract"),
    path('delete-client-contract/', delete_contract, name="delete_contract"),

]
