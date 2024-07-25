from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from human_resources.models import NonSystemUser

User = get_user_model()



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_non_system_user(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone = request.data.get('phone', "")
        job_title = request.data.get('job_title', "")



        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        if not job_title:
            errors['job_title'] = ['Job title is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        user = User.objects.create(
            first_name=first_name,
            last_name=first_name,
            phone=phone,
        )

        non_user = NonSystemUser.objects.create(
            user=user,
            job_title=job_title
        )


        data['user_id'] = user.user_id
        #data['non_user_id'] = non_user.non_user_id




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload)

