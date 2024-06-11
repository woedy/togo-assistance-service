from django.urls import path

from logistics.api.views.assignment_views import add_assignment, edit_assignment, get_all_assignments_view, \
    get_assignment_details_view, archive_assignment, unarchive_assignment, get_all_archived_assignments_view, \
    delete_assignment
from logistics.api.views.category_views import add_category, edit_category, get_all_category_view, \
    get_category_details_view, archive_category, unarchive_category, get_all_archived_categories_view, delete_category
from logistics.api.views.equipments_views import add_equipment, edit_equipment, get_all_equipment_view, \
    get_equipment_details_view, archive_equipment, unarchive_equipment, get_all_archived_equipments_view, \
    delete_equipment
from logistics.api.views.inventory_views import add_inventory, edit_inventory, \
    get_all_inventorys_view, get_inventory_details_view, archive_inventory, unarchive_inventory, \
    get_all_archived_inventorys_view, delete_inventory
from logistics.api.views.maintainance_views import add_maintenance, edit_maintenance, get_all_maintenance_view, \
    get_maintenance_details_view, archive_maintenance, unarchive_maintenance, get_all_archived_maintenances_view, \
    delete_maintenance
from logistics.api.views.order_items_views import add_order_item, edit_order_item, get_all_order_items_view, \
    get_order_item_details_view, archive_order_item, unarchive_order_item, get_all_archived_order_items_view, \
    delete_order_item
from logistics.api.views.order_views import add_order, edit_order, get_all_orders_view, get_order_details_view, \
    archive_order, unarchive_order, get_all_archived_orders_view, delete_order
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

    ########## Inventory ####
    path('add-inventory/', add_inventory, name="add_inventory"),
    path('edit-inventory/', edit_inventory, name="edit_inventory"),
    path('get-all-inventories/', get_all_inventorys_view, name="get_all_inventories_view"),
    path('get-inventory-details/', get_inventory_details_view, name="get_inventory_details_view"),
    path('archive-inventory/', archive_inventory, name="archive_inventory"),
    path('unarchive-inventory/', unarchive_inventory, name="unarchive_inventory"),
    path('get-all-archived-inventories/', get_all_archived_inventorys_view, name="get_all_archived_inventories_view"),
    path('delete-inventory/', delete_inventory, name="delete_inventory"),

    ########## Assignment ####
    path('add-item-assignment/', add_assignment, name="add_assignment"),
    path('edit-item-assignment/', edit_assignment, name="edit_assignment"),
    path('get-all-item-assignment/', get_all_assignments_view, name="get_all_assignments_view"),
    path('get-item-assignment-details/', get_assignment_details_view, name="get_assignment_details_view"),
    path('archive-item-assignment/', archive_assignment, name="archive_assignment"),
    path('unarchive-item-assignment/', unarchive_assignment, name="unarchive_assignment"),
    path('get-all-archived-item-assignments/', get_all_archived_assignments_view, name="get_all_archived_assignments_view"),
    path('delete-item-assignment/', delete_assignment, name="delete_assignment"),

    ########## Order ####
    path('add-order/', add_order, name="add_order"),
    path('edit-order/', edit_order, name="edit_order"),
    path('get-all-orders/', get_all_orders_view, name="get_all_orders_view"),
    path('get-order-details/', get_order_details_view, name="get_order_details_view"),
    path('archive-order/', archive_order, name="archive_order"),
    path('unarchive-order/', unarchive_order, name="unarchive_order"),
    path('get-all-archived-orders/', get_all_archived_orders_view, name="get_all_archived_orders_view"),
    path('delete-order/', delete_order, name="delete_order"),

    ########## Order Item ####
    path('add-order-item/', add_order_item, name="add_order_item"),
    path('edit-order-item/', edit_order_item, name="edit_order_item"),
    path('get-all-order-items/', get_all_order_items_view, name="get_all_order_items_view"),
    path('get-order-items-details/', get_order_item_details_view, name="get_order_items_details_view"),
    path('archive-order-item/', archive_order_item, name="archive_order_item"),
    path('unarchive-order-item/', unarchive_order_item, name="unarchive_order_item"),
    path('get-all-archived-order-items/', get_all_archived_order_items_view, name="get_all_archived_order_items_view"),
    path('delete-order-item/', delete_order_item, name="delete_order_item"),

    ########## Maintnance ####
    path('schedule-maintenance/', add_maintenance, name="schedule_maintenance"),
    path('edit-schedule-maintenance/', edit_maintenance, name="edit_maintenance"),
    path('get-all-schedule-maintenance/', get_all_maintenance_view, name="get_all_maintenance_view"),
    path('get-maintenance-details/', get_maintenance_details_view, name="get_order_items_details_view"),
    path('archive-maintenance/', archive_maintenance, name="archive_maintenance"),
    path('unarchive-maintenance/', unarchive_maintenance, name="unarchive_maintenance"),
    path('get-all-archived-maintenances/', get_all_archived_maintenances_view, name="get_all_archived_order_items_view"),
    path('delete-maintenance/', delete_maintenance, name="delete_maintenance"),

]
