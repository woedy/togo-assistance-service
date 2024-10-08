from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.models import Booking, BookedGuard, ForwardingList, FieldReport, BookingEmail
from clients.api.serializers import AllClientsSerializer
from clients.models import Client
from post_sites.models import ClientZone, ClientPostSite, ClientZoneCoordinate, PostOrder, SiteReport, ZoneCategory
from security_team.api.serializers import SecurityGuardDetailsSerializer

User = get_user_model()



class ForwardingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForwardingList
        fields = ["department"]


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
    client = AllClientsSerializer(many=False)

    class Meta:
        model = Booking
        fields = "__all__"




class AllBookingsSerializer(serializers.ModelSerializer):
    client = AllClientsSerializer(many=False)
    forwarding_list = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"

    def get_forwarding_list(self, obj):
        return [fl.department for fl in obj.forwarding_list.all()]


class ClientZoneCoordinateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientZoneCoordinate
        fields = ["lat", "lng"]




class ClientZoneDetailsSerializer(serializers.ModelSerializer):
    #client = ClientDetailsSerializer(many=False)
    zone_coordinates = ClientZoneCoordinateSerializer(many=True)


    class Meta:
        model = ClientZone
        fields = "__all__"




class AllClientZonesSerializer(serializers.ModelSerializer):
    #client = ClientDetailsSerializer(many=False)
    zone_coordinates = ClientZoneCoordinateSerializer(many=True)

    class Meta:
        model = ClientZone
        fields = "__all__"






class ClientPostSiteDetailsSerializer(serializers.ModelSerializer):
    client_zone = ClientZoneDetailsSerializer(many=False)
    client = ClientDetailsSerializer(many=False)

    class Meta:
        model = ClientPostSite
        fields = "__all__"




class AllClientPostSitesSerializer(serializers.ModelSerializer):
    client_zone = ClientZoneDetailsSerializer(many=False)
    client = ClientDetailsSerializer(many=False)

    class Meta:
        model = ClientPostSite
        fields = "__all__"



class BookedGuardDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookedGuard
        fields = "__all__"




class AllBookedGuardsSerializer(serializers.ModelSerializer):
    guard = SecurityGuardDetailsSerializer(many=False)
    booking = AllBookingsSerializer(many=False)

    class Meta:
        model = BookedGuard
        fields = "__all__"





class FieldReportDetailsSerializer(serializers.ModelSerializer):
    booking = AllBookingsSerializer(many=False)

    class Meta:
        model = FieldReport
        fields = "__all__"




class AllFieldReportsSerializer(serializers.ModelSerializer):
    booking = AllBookingsSerializer(many=False)

    class Meta:
        model = FieldReport
        fields = "__all__"


class AllBookingEmailsSerializer(serializers.ModelSerializer):
    booking = AllBookingsSerializer(many=False)

    class Meta:
        model = BookingEmail
        fields = "__all__"




class PostOrderDetailsSerializer(serializers.ModelSerializer):
    post_site = ClientPostSiteDetailsSerializer(many=False)

    class Meta:
        model = PostOrder
        fields = "__all__"

class AllPostOrdersSerializer(serializers.ModelSerializer):
    post_site = ClientPostSiteDetailsSerializer(many=False)

    class Meta:
        model = PostOrder
        fields = "__all__"





class SiteReportDetailsSerializer(serializers.ModelSerializer):
    post_site = ClientPostSiteDetailsSerializer(many=False)

    class Meta:
        model = SiteReport
        fields = "__all__"

class AllSiteReportsSerializer(serializers.ModelSerializer):
    post_site = ClientPostSiteDetailsSerializer(many=False)

    class Meta:
        model = SiteReport
        fields = "__all__"


class AllZoneCategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ZoneCategory
        fields = "__all__"
