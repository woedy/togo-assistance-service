from django.urls import path

from bookings.api.views import add_client_request_basic_info_view, add_client_request_basic_zone_view, \
    add_client_request_basic_zone_sites_view, add_client_request_date_times_view, get_all_client_requests, \
    get_client_request_details, edit_client_request, edit_client_request_zone, edit_client_request_zone_site, \
    edit_client_request_datetime, archive_client_request, delete_client_request, unarchive_client_request

app_name = 'bookings'

urlpatterns = [
    #path('add-client-request-generic/', add_client_request_generic_view, name="add_client_request_generic_view"),
    path('add-client-request-basic-info/', add_client_request_basic_info_view, name="add_client_request_basic_info_view"),
    path('add-client-request-zone/', add_client_request_basic_zone_view, name="add_client_request_basic_zone_view"),
    path('add-client-request-zone-sites/', add_client_request_basic_zone_sites_view, name="add_client_request_basic_zone_sites_view"),
    path('add-client-request-datetime/', add_client_request_date_times_view, name="add_client_request_basic_zone_sites_view"),

    path('get-all-client-requests/', get_all_client_requests, name="get_all_client_requests"),
    path('get-booking-details/', get_client_request_details, name="get_client_request_details"),
    path('edit-client-request-basic-info/', edit_client_request, name="edit_client_request"),
    path('edit-client-request-zone/', edit_client_request_zone, name="edit_client_request_zone"),
    path('edit-client-request-zone-site/', edit_client_request_zone_site, name="edit_client_request_zone_site"),
    path('edit-client-request-datetime/', edit_client_request_datetime, name="edit_client_request_datetime"),

    path('archive-client-request/', archive_client_request, name="archive_client_request"),
    path('unarchive-client-request/', unarchive_client_request, name="unarchive_client_request"),
    path('delete-client-request/', delete_client_request, name="delete_client_request"),

]
