from django.contrib.auth import get_user_model
from rest_framework import serializers

from logistics.models import Supplier

User = get_user_model()

class SupplierDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"



class AllSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"
