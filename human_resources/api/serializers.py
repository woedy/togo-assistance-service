from django.contrib.auth import get_user_model
from rest_framework import serializers

from human_resources.models import HumanResource

User = get_user_model()


class HumanResourceUserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class HumanResourceDetailsSerializer(serializers.ModelSerializer):
    user = HumanResourceUserDetailSerializer(many=False)
    class Meta:
        model = HumanResource
        fields = "__all__"




