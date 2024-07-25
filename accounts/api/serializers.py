from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserFile

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def save(self):
        user = User(
            email=self.validated_data['email'].lower(),
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],

        )
        password = self.validated_data['password']
        # password2 = self.validated_data['password2']
        # if password != password2:
        #     raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        user.is_active = True
        user.employment_status = 'Employed'
        user.save()

        return user



class StaffRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email',  'first_name', 'last_name',]

    def save(self):
        user = User(
            email=self.validated_data['email'].lower(),
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],

        )
        user.is_active = True
        user.save()

        return user




class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)



class ListAllUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name',  'last_name', 'department', 'photo','phone',]





class AllUserFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = "__all__"


class UserFileDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = "__all__"