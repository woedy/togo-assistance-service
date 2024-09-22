from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save

from communications.models import PrivateChatRoom
from security_team.models import SecurityGuard
from tas_project.utils import unique_assignment_id_generator, unique_category_id_generator, unique_equipment_id_generator, unique_inventory_id_generator, unique_logistics_id_generator, unique_maintenance_id_generator, unique_order_id_generator, unique_order_item_id_generator, unique_site_item_assignment_id_generator, unique_supplier_id_generator

User = get_user_model()



class Logistics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logistics')
    logistics_id = models.CharField(max_length=200, null=True, blank=True)
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name="logistics_user_room")

    profile_complete = models.BooleanField(default=False)

    currently_checked_in = models.BooleanField(default=False)
    last_worked = models.DateTimeField(blank=True, null=True)


    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.email



def pre_save_logistics_id_receiver(sender, instance, *args, **kwargs):
    if not instance.logistics_id:
        instance.logistics_id = unique_logistics_id_generator(instance)

pre_save.connect(pre_save_logistics_id_receiver, sender=Logistics)







class Category(models.Model):
    category_id = models.CharField(max_length=200, null=True, blank=True)

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def pre_save_category_id_receiver(sender, instance, *args, **kwargs):
    if not instance.category_id:
        instance.category_id = unique_category_id_generator(instance)

pre_save.connect(pre_save_category_id_receiver, sender=Category)




class Supplier(models.Model):
    supplier_id = models.CharField(max_length=200, null=True, blank=True)

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



def pre_save_supplier_id_receiver(sender, instance, *args, **kwargs):
    if not instance.supplier_id:
        instance.supplier_id = unique_supplier_id_generator(instance)

pre_save.connect(pre_save_supplier_id_receiver, sender=Supplier)






class Equipment(models.Model):
    equipment_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)

    purchase_date = models.DateField()

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def pre_save_equipment_id_receiver(sender, instance, *args, **kwargs):
    if not instance.equipment_id:
        instance.equipment_id = unique_equipment_id_generator(instance)

pre_save.connect(pre_save_equipment_id_receiver, sender=Equipment)






class Inventory(models.Model):
    inventory_id = models.CharField(max_length=200, null=True, blank=True)

    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"


def pre_save_inventory_id_receiver(sender, instance, *args, **kwargs):
    if not instance.inventory_id:
        instance.inventory_id = unique_inventory_id_generator(instance)

pre_save.connect(pre_save_inventory_id_receiver, sender=Inventory)



class Assignment(models.Model):
    assignment_id = models.CharField(max_length=200, null=True, blank=True)

    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    return_due_date = models.DateField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} to {self.guard}"


def pre_save_assignment_id_receiver(sender, instance, *args, **kwargs):
    if not instance.assignment_id:
        instance.assignment_id = unique_assignment_id_generator(instance)

pre_save.connect(pre_save_assignment_id_receiver, sender=Assignment)



class Order(models.Model):
    order_id = models.CharField(max_length=200, null=True, blank=True)

    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_order_id_receiver, sender=Order)


class OrderItem(models.Model):
    order_item_id = models.CharField(max_length=200, null=True, blank=True)

    order = models.ForeignKey(Order, related_name='equipments', on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def get_total_price(self):
        return self.quantity * self.price



def pre_save_order_item_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_item_id:
        instance.order_item_id = unique_order_item_id_generator(instance)


pre_save.connect(pre_save_order_item_id_receiver, sender=OrderItem)



class Maintenance(models.Model):
    maintenance_id = models.CharField(max_length=200, null=True, blank=True)

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Maintenance for {self.equipment.name} on {self.scheduled_date}'



def pre_save_maintenance_id_receiver(sender, instance, *args, **kwargs):
    if not instance.maintenance_id:
        instance.maintenance_id = unique_maintenance_id_generator(instance)

pre_save.connect(pre_save_maintenance_id_receiver, sender=Maintenance)





class SiteItemAssignment(models.Model):
    site_item_assignment_id = models.CharField(max_length=200, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    return_due_date = models.DateField(blank=True, null=True)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} to {self.user.first_name}"


def pre_save_site_item_assignment_id_receiver(sender, instance, *args, **kwargs):
    if not instance.site_item_assignment_id:
        instance.site_item_assignment_id = unique_site_item_assignment_id_generator(instance)

pre_save.connect(pre_save_site_item_assignment_id_receiver, sender=SiteItemAssignment)




class ItemHistory(models.Model):

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    notes = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=0)

    is_archived = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)