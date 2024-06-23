from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking, BookedGuard
from clients.models import Client, ClientComplaint
from post_sites.models import ClientZone, ClientPostSite
from security_team.api.serializers import SecurityGuardDetailsSerializer

User = get_user_model()


class ClientUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class AllClientsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class ClientDetailsSerializer(serializers.ModelSerializer):
    user = ClientUserDetailSerializer(many=False)
    class Meta:
        model = Client
        fields = "__all__"



class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"




class AllBookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"




class ClientZoneDetailsSerializer(serializers.ModelSerializer):
    client = ClientDetailsSerializer(many=False)

    class Meta:
        model = ClientZone
        fields = "__all__"




class AllClientZonesSerializer(serializers.ModelSerializer):
    client = ClientDetailsSerializer(many=False)

    class Meta:
        model = ClientZone
        fields = "__all__"






class ClientPostSiteDetailsSerializer(serializers.ModelSerializer):
    client_zone = ClientZoneDetailsSerializer(many=False)

    class Meta:
        model = ClientPostSite
        fields = "__all__"




class AllClientPostSitesSerializer(serializers.ModelSerializer):
    client_zone = ClientZoneDetailsSerializer(many=False)

    class Meta:
        model = ClientPostSite
        fields = "__all__"



class BookedGuardDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookedGuard
        fields = "__all__"




class AllBookedGuardsSerializer(serializers.ModelSerializer):
    guard = SecurityGuardDetailsSerializer(many=False)

    class Meta:
        model = BookedGuard
        fields = "__all__"

