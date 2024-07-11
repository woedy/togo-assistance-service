from django.contrib.auth import get_user_model
from rest_framework import serializers

from billing.models import Billing, ClientPayment
from bookings.api.serializers import AllBookingsSerializer
from human_resources.models import HumanResource
from security_team.models import PayPeriod, PayrollEntry

User = get_user_model()


class BillingUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class BillingDetailsSerializer(serializers.ModelSerializer):
    user = BillingUserDetailSerializer(many=False)
    class Meta:
        model = Billing
        fields = "__all__"



class ClientPaymentDetailsSerializer(serializers.ModelSerializer):
    booking = AllBookingsSerializer(many=False)

    class Meta:
        model = ClientPayment
        fields = "__all__"


class AllClientPaymentsSerializer(serializers.ModelSerializer):
    booking = AllBookingsSerializer(many=False)
    class Meta:
        model = ClientPayment
        fields = "__all__"







class PayPeriodDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayPeriod
        fields = "__all__"


class AllPayPeriodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPeriod
        fields = "__all__"





class PayrollEntryDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PayrollEntry
        fields = "__all__"


class AllPayrollEntrysSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollEntry
        fields = "__all__"



