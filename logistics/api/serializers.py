from django.contrib.auth import get_user_model
from rest_framework import serializers

from clients.models import Client, ClientComplaint

User = get_user_model()


class ClientUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class AllClientsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'photo'
        ]


class ClientDetailsSerializer(serializers.ModelSerializer):
    user = ClientUserDetailSerializer(many=False)
    class Meta:
        model = Client
        fields = "__all__"


class AllClientsSerializer(serializers.ModelSerializer):
    user = AllClientsUserSerializer(many=False)
    class Meta:
        model = Client
        fields = [
            'client_id',
            'user',
        ]




class ClientComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientComplaint
        fields = "__all__"
