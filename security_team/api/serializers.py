from django.contrib.auth import get_user_model
from rest_framework import serializers

from security_team.models import SecurityGuard, GuardAvailability, TimeSlot, SecurityGuardFile
from clients.models import Client

User = get_user_model()




class AllGuardFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SecurityGuardFile
        fields = "__all__"



class SecurityGuardUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class SecurityGuardDetailsSerializer(serializers.ModelSerializer):
    user = SecurityGuardUserDetailSerializer(many=False)
    class Meta:
        model = SecurityGuard
        fields = "__all__"






class AllSecurityGuardsSerializer(serializers.ModelSerializer):
    user = SecurityGuardUserDetailSerializer(many=False)
    class Meta:
        model = SecurityGuard
        fields = "__all__"







class OccupantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

class GuardTimeSerializer(serializers.ModelSerializer):
    occupant = OccupantSerializer(many=False)
    time = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['time', 'occupied', 'occupant', ]

    def get_time(self, obj):
        # Format the time as "HH:MM"
        return obj.time.strftime("%H:%M")

class GuardAvailabilitySerializer(serializers.ModelSerializer):

    availability_time_slots = GuardTimeSerializer(many=True)

    class Meta:
        model = GuardAvailability
        fields = ['id', 'slot_date', 'state', 'availability_time_slots']
