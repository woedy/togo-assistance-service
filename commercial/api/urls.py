from django.urls import path

from bookings.api.views import add_client_request_basic_info_view
from commercial.api.views import add_client_request_estimate_view, send_estimate_to_client, \
     get_all_client_estimates, archive_estimate, unarchive_estimate, delete_estimate
app_name = 'commercial'

urlpatterns = [
    path('add-booking-estimate/', add_client_request_estimate_view, name="add_client_request_estimate_view"),
    path('send-booking-estimate/', send_estimate_to_client, name="send_estimate_to_client"),
    path('get-all-client-estimates/', get_all_client_estimates, name="get_all_client_estimates"),
    path('archive-client-estimate/', archive_estimate, name="archive_estimate"),
    path('unarchive-client-estimate/', unarchive_estimate, name="unarchive_estimate"),
    path('delete-client-estimate/', delete_estimate, name="delete_estimate"),

]
