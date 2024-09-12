from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.api.serializers import ListAllUsersSerializer
from clients.models import Client
from secretary.models import Letter, Meeting, Secretary, LogBook
from security_team.models import FileManagement

User = get_user_model()


class SecretaryUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class SecretaryDetailsSerializer(serializers.ModelSerializer):
    user = SecretaryUserDetailSerializer(many=False)
    class Meta:
        model = Secretary
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    user = SecretaryUserDetailSerializer(many=False)

    class Meta:
        model = Client
        fields = "__all__"




class AllLogBookSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=False)

    class Meta:
        model = LogBook
        fields = "__all__"









class AllFilesSerializer(serializers.ModelSerializer):
    file_forwarding_list = serializers.SerializerMethodField()

    class Meta:
        model = FileManagement
        fields = "__all__"


    
    def get_file_forwarding_list(self, obj):
        return [fl.department for fl in obj.file_forwarding_list.all()]





class AllMeetingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        fields = "__all__"




class MeetingDetailsSerializer(serializers.ModelSerializer):
    attendees = ListAllUsersSerializer(many=True)

    meeting_attendees = ListAllUsersSerializer(many=True)


    class Meta:
        model = Meeting
        fields = "__all__"









class AllLettersSerializer(serializers.ModelSerializer):


    class Meta:
        model = Letter
        fields = "__all__"




class LetterDetailsSerializer(serializers.ModelSerializer):
    sender = ListAllUsersSerializer(many=False)
    receiver = ListAllUsersSerializer(many=False)


    class Meta:
        model = Letter
        fields = "__all__"


