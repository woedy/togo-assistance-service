from django.urls import path

from billing.api.client_payment_views import add_client_payment, edit_client_payment, get_all_client_payments_view, \
    get_client_payment_details_view, archive_client_payment, unarchive_client_payment, delete_client_payment, \
    get_all_archived_client_payments_view
from billing.api.guard_pay_period_views import add_pay_period, get_all_pay_period_view, get_pay_period_details_view, \
    edit_pay_period, archive_pay_period, delete_pay_period, unarchive_pay_period, get_all_archived_pay_period_view
from billing.api.guard_payroll_entery_views import add_payroll_entry, get_all_payroll_entry_view, \
    get_payroll_entry_details_view, edit_payroll_entry, archive_payroll_entry, delete_payroll_entry, \
    unarchive_payroll_entry, get_all_archived_payroll_entry_view
from billing.api.views import get_billing_dashboard
from human_resources.api.views import get_hr_dashboard

app_name = 'billing'

urlpatterns = [
    path('get-billing-dashboard/', get_billing_dashboard, name="get_billing_dashboard"),




    ### Client Payments
    path('add-client-payment/', add_client_payment, name="add_client_payment"),
    path('edit-client-payment/', edit_client_payment, name="edit_client_payment"),
    path('get-all-client-payments/', get_all_client_payments_view, name="get_all_client_payments_view"),
    path('get-client-payment-details/', get_client_payment_details_view, name="get_client_payment_details_view"),
    path('archive-client-payment/', archive_client_payment, name="archive_client_payment"),
    path('unarchive-client-payment/', unarchive_client_payment, name="unarchive_client_payment"),
    path('delete-client-payment/', delete_client_payment, name="delete_client_payment"),
    path('get-all-archived-client-payments/', get_all_archived_client_payments_view,
         name="get_all_archived_client_payments_view"),

    ### Guard Pay Period
    path('add-pay-period/', add_pay_period, name="add_pay_period"),
    path('edit-pay-period/', edit_pay_period, name="edit_pay_period"),
    path('get-all-pay-periods/', get_all_pay_period_view, name="get_all_pay_period_view"),
    path('get-pay-period-details/', get_pay_period_details_view, name="get_pay_period_details_view"),
    path('archive-pay-period/', archive_pay_period, name="archive_pay_period"),
    path('unarchive-pay-period/', unarchive_pay_period, name="unarchive_pay_period"),
    path('delete-pay-period/', delete_pay_period, name="delete_pay_period"),
    path('get-all-archived-pay-periods/', get_all_archived_pay_period_view,
         name="get_all_archived_pay_period_view"),

    ### Guard Payroll Entry
    path('add-payroll-entry/', add_payroll_entry, name="add_payroll_entry"),
    path('edit-payroll-entry/', edit_payroll_entry, name="edit_payroll_entry"),
    path('get-all-payroll-entries/', get_all_payroll_entry_view, name="get_all_payroll_entry_view"),
    path('get-payroll-entry-details/', get_payroll_entry_details_view, name="get_payroll_entry_details_view"),
    path('archive-payroll-entry/', archive_payroll_entry, name="archive_payroll_entry"),
    path('unarchive-payroll-entry/', unarchive_payroll_entry, name="unarchive_payroll_entry"),
    path('delete-payroll-entry/', delete_payroll_entry, name="delete_payroll_entry"),
    path('get-all-archived-payroll-entries/', get_all_archived_payroll_entry_view,
         name="get_all_archived_pay_period_view"),

]
