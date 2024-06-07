from django.urls import path

from logistics.api.views import add_supplier, edit_supplier, get_all_supplier_view, get_supplier_details_view, \
    archive_supplier, delete_supplier, unarchive_supplier, get_all_archived_suppliers_view

app_name = 'logistics'

urlpatterns = [
    path('add-supplier/', add_supplier, name="add_supplier"),
    path('edit-supplier/', edit_supplier, name="edit_supplier"),
    path('get-all-suppliers/', get_all_supplier_view, name="get_all_suppliers_view"),
    path('get-supplier-details/', get_supplier_details_view, name="get_supplier_details_view"),
    path('archive-supplier/', archive_supplier, name="archive_supplier"),
    path('delete-supplier/', delete_supplier, name="delete_supplier"),
    path('unarchive-supplier/', unarchive_supplier, name="unarchive_supplier"),
    path('get-all-archived-suppliers/', get_all_archived_suppliers_view, name="get_all_archived_suppliers_view"),


]
