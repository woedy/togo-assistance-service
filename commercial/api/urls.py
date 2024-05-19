from django.urls import path

from bookings.api.views import add_client_request_basic_info_view

app_name = 'bookings'

urlpatterns = [
    #path('add-client-request-generic/', add_client_request_generic_view, name="add_client_request_generic_view"),
    path('add-booking-estimate/', add_booking_estimate_view, name="add_booking_estimate_view"),

]
