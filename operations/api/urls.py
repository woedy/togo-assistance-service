from django.urls import path
from human_resources.api.views import get_hr_dashboard
from operations.api.attendance_views import clock_in_guard, get_all_attendances, get_attendance_details_view, \
    archive_attendance, delete_attendance, unarchive_attendance, get_all_archived_attendances_view, clock_out_guard
from operations.api.deployment_views import assign_supervisor, get_all_deployments, get_all_supervisors, get_deployment_details_view, \
    archive_deployment, delete_deployment, unarchive_deployment, get_all_archived_deployments_view, deploy_team
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

]
