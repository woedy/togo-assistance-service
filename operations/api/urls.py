from django.urls import path
from human_resources.api.views import get_hr_dashboard
from operations.api.attendance_views import clock_in_guard, get_all_attendances, get_attendance_details_view, \
    archive_attendance, delete_attendance, unarchive_attendance, get_all_archived_attendances_view, clock_out_guard
from operations.api.deployment_views import assign_supervisor, get_all_deployments, get_all_supervisors, get_deployment_details_view, \
    archive_deployment, delete_deployment, unarchive_deployment, get_all_archived_deployments_view, deploy_team
from operations.api.panic_alert_view import add_panic_report, archive_panic_report, change_panic_report_status, delete_panic_report, get_all_panic_reports_view, get_all_unarchived_panic_reports_view, get_panic_report_details_view, unarchive_panic_report
from operations.api.site_alert_view import add_site_alert, archive_site_alert, change_site_alert_status, delete_site_alert, get_all_site_alerts_view, get_all_unarchived_site_alerts_view, site_alert_response, unarchive_site_alert
from operations.api.views import get_operations_dashboard, update_role

app_name = 'operations'

urlpatterns = [
    path('get-operations-dashboard/', get_operations_dashboard, name="get_operations_dashboard"),
    path('update-role/', update_role, name="update_role"),

    path('assign-supervisor/', assign_supervisor, name="assign_supervisor"),
    path('deploy-team/', deploy_team, name="deploy_team"),
    path('get-all-deployments/', get_all_deployments, name="get_all_deployments"),

    path('get-all-supervisors/', get_all_supervisors, name="get_all_supervisors"),
    path('get-deployment-details/', get_deployment_details_view, name="get_deployment_details_view"),
    path('archive-deployment/', archive_deployment, name="archive_deployment"),
    path('delete-deployment/', delete_deployment, name="delete_deployment"),
    path('unarchive-deployment/', unarchive_deployment, name="unarchive_deployment"),
    path('get-all-archived-deployments/', get_all_archived_deployments_view, name="get_all_archived_deployments_view"),

    path('clock-in-guard/', clock_in_guard, name="clock_in_guard"),
    path('clock-out-guard/', clock_out_guard, name="clock_out_guard"),
    path('get-all-attendances/', get_all_attendances, name="get_all_attendances"),
    path('get-attendance-details/', get_attendance_details_view, name="get_attendance_details_view"),
    path('archive-attendance/', archive_attendance, name="archive_attendance"),
    path('delete-attendance/', delete_attendance, name="delete_attendance"),
    path('unarchive-attendance/', unarchive_attendance, name="unarchive_attendance"),
    path('get-all-archived-attendances/', get_all_archived_attendances_view, name="get_all_archived_attendances_view"),

    path('add-panic-report/', add_panic_report, name="add_panic_report"),
    #path('edit-panic_report/', edit_panic_report, name="edit_panic_report"),
    path('get-all-panic-reports/', get_all_panic_reports_view, name="get_all_panic_reports_view"),
    #path('get-panic-report-details/', get_panic_report_details_view, name="get_panic_report_details_view"),
    path('archive-panic-report/', archive_panic_report, name="archive_panic_report"),
    path('delete-panic-report/', delete_panic_report, name="delete_panic_report"),
    path('unarchive-panic-report/', unarchive_panic_report, name="unarchive_panic_report"),
    path('get-all-archived-panic-reports/', get_all_unarchived_panic_reports_view, name="get_all_archived_panic_reports_view"),
    path('change-panic-report-status/', change_panic_report_status, name="change_panic_report_status"),




    path('add-site-alert/', add_site_alert, name="add_site_alert"),
    #path('edit-site_alert/', edit_site_alert, name="edit_site_alert"),
    path('get-all-site-alerts/', get_all_site_alerts_view, name="get_all_site_alerts_view"),
    ##path('get-site-alert-details/', get_site_alert_details_view, name="get_site_alert_details_view"),
    path('archive-site-alert/', archive_site_alert, name="archive_site_alert"),
    path('delete-site-alert/', delete_site_alert, name="delete_site_alert"),
    path('unarchive-site-alert/', unarchive_site_alert, name="unarchive_site_alert"),
    path('get-all-archived-site-alerts/', get_all_unarchived_site_alerts_view, name="get_all_archived_site_alerts_view"),
    path('change-site-alert-status/', change_site_alert_status, name="change_site_alert_status"),
    path('site-alert-response/', site_alert_response, name="site_alert_response"),

]
