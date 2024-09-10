from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking
from bookings.models import Estimate
from commercial.models import Commercial
from clients.api.serializers import AllClientsSerializer

User = get_user_model()

class AllBookingsSerializer(serializers.ModelSerializer):
    client = AllClientsSerializer(many=False)
    forwarding_list = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"

    def get_forwarding_list(self, obj):
        return [fl.department for fl in obj.forwarding_list.all()]


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
    booking = AllBookingsSerializer(many=False)
    class Meta:
        model = Estimate
        fields = "__all__"



