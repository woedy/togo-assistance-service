from django.urls import path

from human_resources.api.staff_pay_period_views import add_staff_pay_period, edit_staff_pay_period, \
    get_all_staff_pay_period_view, get_pay_staff_period_details_view, archive_staff_pay_period, \
    unarchive_staff_pay_period, delete_staff_pay_period, get_all_archived_staff_pay_period_view
from human_resources.api.staff_payroll_entery_views import add_staff_payroll_entry, edit_staff_payroll_entry, \
    get_all_staff_payroll_entry_view, get_staff_payroll_entry_details_view, archive_staff_payroll_entry, \
    unarchive_staff_payroll_entry, delete_staff_payroll_entry, get_all_archived_staff_payroll_entry_view
from human_resources.api.views import get_hr_dashboard

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
]
