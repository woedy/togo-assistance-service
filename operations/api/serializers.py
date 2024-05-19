from django.contrib.auth import get_user_model
from rest_framework import serializers

from operations.models import Operation

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




