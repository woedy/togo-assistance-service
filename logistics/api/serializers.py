from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.api.serializers import ListAllUsersSerializer
from logistics.models import SiteItemAssignment, Supplier, Category, OrderItem, Equipment, Inventory, Assignment, Order, Maintenance
from security_team.api.serializers import SecurityGuardDetailsSerializer

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


class EquipmentDetailsSerializer(serializers.ModelSerializer):
    category = AllCategorySerializer(many=False)
    supplier = AllSupplierSerializer(many=False)
    class Meta:
        model = Equipment
        fields = "__all__"



class AllEquipmentSerializer(serializers.ModelSerializer):
    category = AllCategorySerializer(many=False)
    supplier = AllSupplierSerializer(many=False)
    class Meta:
        model = Equipment
        fields = "__all__"




class InventoryDetailsSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)


    class Meta:
        model = Inventory
        fields = "__all__"



class AllInventorySerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)

    class Meta:
        model = Inventory
        fields = "__all__"


class AssignmentDetailsSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)
    guard = SecurityGuardDetailsSerializer(many=False)

    class Meta:
        model = Assignment
        fields = "__all__"



class AllAssignmentSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)
    guard = SecurityGuardDetailsSerializer(many=False)
    class Meta:
        model = Assignment
        fields = "__all__"


class OrderDetailsSerializer(serializers.ModelSerializer):
    supplier = AllSupplierSerializer(many=False)

    class Meta:
        model = Order
        fields = "__all__"



class AllOrderSerializer(serializers.ModelSerializer):
    supplier = AllSupplierSerializer(many=False)

    class Meta:
        model = Order
        fields = "__all__"


class MaintenanceDetailsSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)

    class Meta:
        model = Maintenance
        fields = "__all__"



class AllMaintenanceSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)

    class Meta:
        model = Maintenance
        fields = "__all__"



class OrderItemDetailsSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)
    order = AllOrderSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = "__all__"



class AllOrderItemSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)
    order = AllOrderSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = "__all__"





class SiteItemAssignmentDetailsSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)
    user = ListAllUsersSerializer(many=False)

    class Meta:
        model = SiteItemAssignment
        fields = "__all__"



class AllSiteItemAssignmentSerializer(serializers.ModelSerializer):
    equipment = AllEquipmentSerializer(many=False)
    user = ListAllUsersSerializer(many=False)
    class Meta:
        model = SiteItemAssignment
        fields = "__all__"
