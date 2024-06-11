from django.contrib import admin

from logistics.models import Category, Supplier, Equipment, Inventory, Order, OrderItem, Maintenance

admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Equipment)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Maintenance)
