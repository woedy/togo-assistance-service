from django.contrib.auth import get_user_model
from rest_framework import serializers

from billing.models import Billing
from human_resources.models import HumanResource

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




