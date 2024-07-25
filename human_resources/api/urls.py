from django.urls import path

from human_resources.api.non_system_user_views import add_non_system_user
from human_resources.api.recruitment_attachment_views import get_all_archived_recruitment_attachments_view, \
    add_recruitment_attachment, get_all_recruitment_attachments_view, archive_recruitment_attachment, \
    get_recruitment_attachment_details_view, delete_recruitment_attachment, unarchive_recruitment_attachment
from human_resources.api.recruitment_views import add_recruitment, edit_recruitment, get_all_recruitments_view, \
    get_recruitment_details_view, archive_recruitment, delete_recruitment, unarchive_recruitment, \
    get_all_archived_recruitments_view
from human_resources.api.staff_pay_period_views import add_staff_pay_period, edit_staff_pay_period, \
    get_all_staff_pay_period_view, get_pay_staff_period_details_view, archive_staff_pay_period, \
    unarchive_staff_pay_period, delete_staff_pay_period, get_all_archived_staff_pay_period_view
from human_resources.api.staff_payroll_entery_views import add_staff_payroll_entry, edit_staff_payroll_entry, \
    get_all_staff_payroll_entry_view, get_staff_payroll_entry_details_view, archive_staff_payroll_entry, \
    unarchive_staff_payroll_entry, delete_staff_payroll_entry, get_all_archived_staff_payroll_entry_view
from human_resources.api.views import get_hr_dashboard, change_employment_status

app_name = 'human_resources'

urlpatterns = [
    path('get-hr-dashboard/', get_hr_dashboard, name="get_hr_dashboard"),


### Staff Pay Period
    path('add-staff-pay-period/', add_staff_pay_period, name="add_staff_pay_period"),
    path('edit-staff-pay-period/', edit_staff_pay_period, name="edit_staff_pay_period"),
    path('get-all-staff-pay-periods/', get_all_staff_pay_period_view, name="get_all_staff_pay_period_view"),
    path('get-staff-pay-period-details/', get_pay_staff_period_details_view, name="get_staff_pay_period_details_view"),
    path('archive-staff-pay-period/', archive_staff_pay_period, name="archive_staff_pay_period"),
    path('unarchive-staff-pay-period/', unarchive_staff_pay_period, name="unarchive_staff_pay_period"),
    path('delete-staff-pay-period/', delete_staff_pay_period, name="delete_staff_pay_period"),
    path('get-all-archived-staff-pay-periods/', get_all_archived_staff_pay_period_view,
         name="get_all_archived_staff_pay_period_view"),

    ### Staff Payroll Entry
    path('add-staff-payroll-entry/', add_staff_payroll_entry, name="add_staff_payroll_entry"),
    path('edit-staff-payroll-entry/', edit_staff_payroll_entry, name="edit_staff_payroll_entry"),
    path('get-all-staff-payroll-entries/', get_all_staff_payroll_entry_view, name="get_all_staff_payroll_entry_view"),
    path('get-staff-payroll-entry-details/', get_staff_payroll_entry_details_view, name="get_staff_payroll_entry_details_view"),
    path('archive-staff-payroll-entry/', archive_staff_payroll_entry, name="archive_staff_payroll_entry"),
    path('unarchive-staff-payroll-entry/', unarchive_staff_payroll_entry, name="unarchive_staff_payroll_entry"),
    path('delete-staff-payroll-entry/', delete_staff_payroll_entry, name="delete_staff_payroll_entry"),
    path('get-all-archived-staff-payroll-entries/', get_all_archived_staff_payroll_entry_view,
         name="get_all_archived_staff_pay_period_view"),

    path('change-employment-status', change_employment_status, name="change_employment_status"),

    path('add-recruitment/', add_recruitment, name="add_recruitment"),
    path('edit-recruitment/', edit_recruitment, name="edit_recruitment"),
    path('get-all-recruitments/', get_all_recruitments_view, name="get_all_recruitments_view"),
    path('get-recruitment-details/', get_recruitment_details_view, name="get_recruitment_details_view"),
    path('archive-recruitment/', archive_recruitment, name="archive_recruitment"),
    path('delete-recruitment/', delete_recruitment, name="delete_recruitment"),
    path('unarchive-recruitment/', unarchive_recruitment, name="unarchive_recruitment"),
    path('get-all-archived-recruitments/', get_all_archived_recruitments_view, name="get_all_archived_recruitments_view"),

    path('add-recruitment-attachment/', add_recruitment_attachment, name="add_recruitment_attachment"),
    path('get-all-recruitment-attachments/', get_all_recruitment_attachments_view, name="get_all_recruitment_attachments_view"),
    path('get-recruitment-details-attachment/', get_recruitment_attachment_details_view, name="get_recruitment_attachment_details_view"),
    path('archive-recruitment-attachment/', archive_recruitment_attachment, name="archive_recruitment_attachment"),
    path('delete-recruitment-attachment/', delete_recruitment_attachment, name="delete_recruitment_attachment"),
    path('unarchive-recruitment-attachment/', unarchive_recruitment_attachment, name="unarchive_recruitment_attachment"),
    path('get-all-archived-recruitment-attachments/', get_all_archived_recruitment_attachments_view,
         name="get_all_archived_recruitment_attachments_view"),

    path('add-non-system-user/', add_non_system_user, name="add_non_system_user"),

]
