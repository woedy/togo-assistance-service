from django.urls import path

from logistics.api.views.category_views import add_category, edit_category, get_all_category_view, \
    get_category_details_view, archive_category, unarchive_category, get_all_archived_categories_view, delete_category
from logistics.api.views.equipments_views import add_equipment, edit_equipment, get_all_equipment_view, \
    get_equipment_details_view, archive_equipment, unarchive_equipment, get_all_archived_equipments_view, \
    delete_equipment
from logistics.api.views.supply_views import add_supplier, edit_supplier, get_all_supplier_view, get_supplier_details_view, \
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


    ########## Categories ####
    path('add-category/', add_category, name="add_category"),
    path('edit-category/', edit_category, name="edit_category"),
    path('get-all-categories/', get_all_category_view, name="get_all_category_view"),
    path('get-category-details/', get_category_details_view, name="get_category_details_view"),
    path('archive-category/', archive_category, name="archive_category"),
    path('unarchive-category/', unarchive_category, name="unarchive_category"),
    path('get-all-archived-category/', get_all_archived_categories_view, name="get_all_archived_categories_view"),
    path('delete-category/', delete_category, name="delete_category"),

    ########## Equipments ####
    path('add-equipment/', add_equipment, name="add_equipment"),
    path('edit-equipment/', edit_equipment, name="edit_equipment"),
    path('get-all-equipments/', get_all_equipment_view, name="get_all_equipment_view"),
    path('get-equipment-details/', get_equipment_details_view, name="get_equipments_details_view"),
    path('archive-equipment/', archive_equipment, name="archive_equipment"),
    path('unarchive-equipment/', unarchive_equipment, name="unarchive_equipment"),
    path('get-all-archived-equipments/', get_all_archived_equipments_view, name="get_all_archived_equipment_view"),
    path('delete-equipment/', delete_equipment, name="delete_equipment"),

]
