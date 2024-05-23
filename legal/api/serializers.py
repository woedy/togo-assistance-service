from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Estimate
from commercial.models import Commercial
from legal.models import Legal
from operations.models import Operation

User = get_user_model()


class LegalUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class LegalDetailsSerializer(serializers.ModelSerializer):
    user = LegalUserDetailSerializer(many=False)
    class Meta:
        model = Legal
        fields = "__all__"




class AllContractsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"



