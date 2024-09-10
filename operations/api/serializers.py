from django.contrib.auth import get_user_model
from rest_framework import serializers

from bookings.api.serializers import BookingDetailsSerializer
from bookings.models import Deployment, DeploymentAttendance
from operations.models import Operation
from security_team.api.serializers import SecurityGuardDetailsSerializer
from clients.models import Client, ClientComplaint
from post_sites.models import ClientZone, ClientPostSite, ClientZoneCoordinate, PostOrder, SiteReport

User = get_user_model()


class OperationUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class OperationsDetailsSerializer(serializers.ModelSerializer):
    user = OperationUserDetailSerializer(many=False)
    class Meta:
        model = Operation
        fields = "__all__"

class ClientUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class ClientDetailsSerializer(serializers.ModelSerializer):
    user = ClientUserDetailSerializer(many=False)
    class Meta:
        model = Client
        fields = "__all__"




class DeploymentDetailsSerializer(serializers.ModelSerializer):
    supervisor = OperationsDetailsSerializer(many=False)

    class Meta:
        model = Deployment
        fields = "__all__"

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



class ClientPostSiteDetailsSerializer(serializers.ModelSerializer):
    client_zone = ClientZoneDetailsSerializer(many=False)
    client = ClientDetailsSerializer(many=False)

    class Meta:
        model = ClientPostSite
        fields = "__all__"



class AllDeploymentsSerializer(serializers.ModelSerializer):
    supervisor = OperationsDetailsSerializer(many=False)
    booking = BookingDetailsSerializer(many=False)
    site = ClientPostSiteDetailsSerializer(many=False)
    guards = SecurityGuardDetailsSerializer(many=True)
    class Meta:
        model = Deployment
        fields = "__all__"





class DeploymentAttendanceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentAttendance
        fields = "__all__"


class AllDeploymentAttendancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentAttendance
        fields = "__all__"


