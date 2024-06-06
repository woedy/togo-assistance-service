from django.db import models
from django.db.models.signals import pre_save

from security_team.models import SecurityGuard
from tas_project.utils import unique_supplier_id_generator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    supplier_id = models.CharField(max_length=200, null=True, blank=True)

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name



def pre_save_supplier_id_receiver(sender, instance, *args, **kwargs):
    if not instance.supplier_id:
        instance.supplier_id = unique_supplier_id_generator(instance)

pre_save.connect(pre_save_supplier_id_receiver, sender=Supplier)






class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=100, unique=True)
    serial_number = models.CharField(max_length=100, unique=True)
    last_maintenance = models.DateField(null=True, blank=True)

    purchase_date = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Inventory(models.Model):
    equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity}"



class Assignment(models.Model):
    guard = models.ForeignKey(SecurityGuard, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    assigned_at = models.DateTimeField(auto_now_add=True)
    return_due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} to {self.guard}"

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='equipments', on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def get_total_price(self):
        return self.quantity * self.price

class Maintenance(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'Maintenance for {self.equipment.name} on {self.scheduled_date}'