
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email, check_email_exist
from activities.models import AllActivity
from clients.api.serializers import AllClientsSerializer, ClientDetailsSerializer

from clients.models import Client, ClientComplaint
from reports.models import Report

User = get_user_model()

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_internal_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        title = request.data.get('title', "")
        report = request.data.get('report', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not title:
            errors['title'] = ['Title is required.']

        if not report:
            errors['report'] = ['Report is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_report = Report.objects.create(
            user=user,
            title=title,
            report=report,
        )


        data["report"] = new_report.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)
