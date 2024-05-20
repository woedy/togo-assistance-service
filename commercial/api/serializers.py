from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Estimate
from commercial.models import Commercial, Contract
from operations.models import Operation

User = get_user_model()


class CommercialUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class CommercialDetailsSerializer(serializers.ModelSerializer):
    user = CommercialUserDetailSerializer(many=False)
    class Meta:
        model = Commercial
        fields = "__all__"



class AllEstimatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = "__all__"



class AllContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"



