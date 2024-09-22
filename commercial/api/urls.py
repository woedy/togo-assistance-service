from django.urls import path

from bookings.api.views import add_client_request_basic_info_view
from commercial.api.views import accept_invoice_view, add_client_request_estimate_view, add_tax_view, delete_tax_view, get_all_client_invoices, get_tax_view, send_estimate_to_client, \
     get_all_client_estimates, archive_estimate, unarchive_estimate, delete_estimate
app_name = 'commercial'

urlpatterns = [
    path('add-booking-estimate/', add_client_request_estimate_view, name="add_client_request_estimate_view"),
    path('send-booking-estimate/', send_estimate_to_client, name="send_estimate_to_client"),
    path('get-all-client-estimates/', get_all_client_estimates, name="get_all_client_estimates"),
    path('get-all-client-invoices/', get_all_client_invoices, name="get_all_client_invoices"),
    path('accept-invoice/', accept_invoice_view, name="accept_invoice_view"),

    path('archive-client-estimate/', archive_estimate, name="archive_estimate"),
    path('unarchive-client-estimate/', unarchive_estimate, name="unarchive_estimate"),
    path('delete-client-estimate/', delete_estimate, name="delete_estimate"),


        path('add-tax/', add_tax_view, name="add_tax_view"),
        path('get-tax/', get_tax_view, name="get_tax_view"),
        path('delete-tax/', delete_tax_view, name="delete_tax_view"),





]
