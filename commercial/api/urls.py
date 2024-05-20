from django.urls import path

from bookings.api.views import add_client_request_basic_info_view
from commercial.api.views import add_client_request_estimate_view, send_estimate_to_client, \
    add_client_request_contract_view, get_all_client_estimates, archive_estimate, unarchive_estimate, delete_estimate, \
    get_all_client_contracts, archive_contract, unarchive_contract, delete_contract

app_name = 'commercial'

urlpatterns = [
    path('add-booking-estimate/', add_client_request_estimate_view, name="add_client_request_estimate_view"),
    path('send-booking-estimate/', send_estimate_to_client, name="send_estimate_to_client"),
    path('add-booking-contract/', add_client_request_contract_view, name="send_estimate_to_client"),
    path('get-all-client-estimates/', get_all_client_estimates, name="get_all_client_estimates"),
    path('get-all-client-contracts/', get_all_client_contracts, name="get_all_client_contracts"),
    path('archive-client-estimate/', archive_estimate, name="archive_estimate"),
    path('archive-client-contract/', archive_contract, name="archive_contract"),
    path('unarchive-client-contract/', unarchive_contract, name="unarchive_contract"),
    path('unarchive-client-estimate/', unarchive_estimate, name="unarchive_estimate"),
    path('delete-client-estimate/', delete_estimate, name="delete_estimate"),
    path('delete-client-contract/', delete_contract, name="delete_contract"),

]
