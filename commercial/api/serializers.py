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
    total_ht = serializers.SerializerMethodField()
    total_tva = serializers.SerializerMethodField()
    total_ttc = serializers.SerializerMethodField()




    class Meta:
        model = Estimate
        fields = "__all__"

    def get_total_ht(self, obj):
        total_ht = obj.total_ht
        return total_ht if total_ht else None



    def get_total_tva(self, obj):
        total_tva = obj.total_tva 
        return total_tva if total_tva else None




    def get_total_ttc(self, obj):
        total_ttc = obj.total_ttc 
        return total_ttc if total_ttc else None


