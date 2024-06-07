from django.contrib.auth import get_user_model
from rest_framework import serializers

from logistics.models import Supplier, Category, OrderItem, Equipment, Inventory, Assignment, Order, Maintenance

User = get_user_model()

class SupplierDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"



class AllSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"





class CategoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class AllCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class OrderItemDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"



class AllOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

class EquipmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"



class AllEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"




class InventoryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"



class AllInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class AssignmentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"



class AllAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"



class AllOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class MaintenanceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"



class AllMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = "__all__"
