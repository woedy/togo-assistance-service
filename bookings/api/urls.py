from django.urls import path

from bookings.api.assign_site_views import assign_guard, unassign_guard, re_assign_guard, get_all_assigned_guards
from bookings.api.field_report_views import add_field_report, edit_field_report, get_all_field_reports_view, \
    get_field_report_details_view, archive_field_report, delete_field_report, unarchive_field_report, \
    get_all_archived_field_reports_view
from bookings.api.views import add_client_request_basic_info_view, add_client_request_basic_zone_view, \
    add_client_request_basic_zone_sites_view, add_client_request_date_times_view, get_all_client_requests, \
    get_client_request_details, edit_client_request, edit_client_request_zone, edit_client_request_zone_site, \
    edit_client_request_datetime, archive_client_request, delete_client_request, unarchive_client_request, \
    get_all_client_request_zones, get_all_client_zone_sites, get_zone_details_view, archive_zone, \
    get_all_archived_zones, unarchive_zone, delete_zone, get_site_details_view, archive_site, get_all_archived_sites, \
    unarchive_site, delete_site, forward_to_department

app_name = 'bookings'

urlpatterns = [
    #path('add-client-request-generic/', add_client_request_generic_view, name="add_client_request_generic_view"),
    path('add-client-request-basic-info/', add_client_request_basic_info_view, name="add_client_request_basic_info_view"),
    path('add-client-request-zone/', add_client_request_basic_zone_view, name="add_client_request_basic_zone_view"),
    path('add-client-request-zone-sites/', add_client_request_basic_zone_sites_view, name="add_client_request_basic_zone_sites_view"),
    path('add-client-request-datetime/', add_client_request_date_times_view, name="add_client_request_basic_zone_sites_view"),

    path('forward-to/', forward_to_department,
         name="forward_to_department"),

    path('get-all-client-requests/', get_all_client_requests, name="get_all_client_requests"),
    path('get-booking-details/', get_client_request_details, name="get_client_request_details"),
    path('edit-client-request-basic-info/', edit_client_request, name="edit_client_request"),
    path('edit-client-request-zone/', edit_client_request_zone, name="edit_client_request_zone"),
    path('edit-client-request-zone-site/', edit_client_request_zone_site, name="edit_client_request_zone_site"),
    path('edit-client-request-datetime/', edit_client_request_datetime, name="edit_client_request_datetime"),

    path('archive-client-request/', archive_client_request, name="archive_client_request"),
    path('unarchive-client-request/', unarchive_client_request, name="unarchive_client_request"),
    path('delete-client-request/', delete_client_request, name="delete_client_request"),

    ##ZONE
    path('get-all-client-request-zones/', get_all_client_request_zones, name="get_all_client_request_zones"),
    path('get-zone-details/', get_zone_details_view, name="get_zone_details_view"),
    path('archive-zone/', archive_zone, name="archive_zone"),
    path('unarchive-zone/', unarchive_zone, name="unarchive_zone"),
    path('get-all-archived-zones/', get_all_archived_zones, name="get_all_archived_zones"),
    path('delete-zone/', delete_zone, name="delete_zone"),

    path('get-all-client-zone-sites/', get_all_client_zone_sites, name="get_all_client_zone_sites"),
    path('get-site-details/', get_site_details_view, name="get_site_details_view"),
    path('archive-site/', archive_site, name="archive_site"),
    path('unarchive-site/', unarchive_site, name="unarchive_site"),
    path('get-all-archived-sites/', get_all_archived_sites, name="get_all_archived_sites"),
    path('delete-site/', delete_site, name="delete_site"),





    path('assign-guard/', assign_guard, name="assign_guard"),
    path('unassign-guard/', unassign_guard, name="unassign_guard"),
    path('re-assign-guard/', re_assign_guard, name="re_assign_guard"),
    path('get-all-assigned-guards/', get_all_assigned_guards, name="get_all_assigned_guards"),


    ##### Field Report

    path('add-field_report/', add_field_report, name="add_field_report"),
    path('edit-field-report/', edit_field_report, name="edit_field_report"),
    path('get-all-field-reports/', get_all_field_reports_view, name="get_all_field_reports_view"),
    path('get-field-report-details/', get_field_report_details_view, name="get_field_report_details_view"),
    path('archive-field-report/', archive_field_report, name="archive_field_report"),
    path('delete-field-report/', delete_field_report, name="delete_field_report"),
    path('unarchive-field-report/', unarchive_field_report, name="unarchive_field_report"),
    path('get-all-archived-field-reports/', get_all_archived_field_reports_view, name="get_all_archived_field_reports_view"),

]
