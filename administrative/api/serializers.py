from django.contrib.auth import get_user_model
from rest_framework import serializers

from administrative.models import AdminDepartment

User = get_user_model()


class AdminDepartmentUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class AdminDepartmentDetailsSerializer(serializers.ModelSerializer):
    user = AdminDepartmentUserDetailSerializer(many=False)
    class Meta:
        model = AdminDepartment
        fields = "__all__"




