from django.contrib.auth import get_user_model
from rest_framework import serializers

from human_resources.models import HumanResource, StaffPayrollEntry, StaffPayPeriod

User = get_user_model()


class HumanResourceUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class HumanResourceDetailsSerializer(serializers.ModelSerializer):
    user = HumanResourceUserDetailSerializer(many=False)
    class Meta:
        model = HumanResource
        fields = "__all__"








class StaffPayPeriodDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffPayPeriod
        fields = "__all__"


class AllStaffPayPeriodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayPeriod
        fields = "__all__"





class StaffPayrollEntryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffPayrollEntry
        fields = "__all__"


class AllStaffPayrollEntrysSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffPayrollEntry
        fields = "__all__"


