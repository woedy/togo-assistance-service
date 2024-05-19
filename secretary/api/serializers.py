from django.contrib.auth import get_user_model
from rest_framework import serializers

from clients.models import Client
from secretary.models import Secretary

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




