
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from clients.api.serializers import ClientDetailsSerializer, ClientComplaintSerializer

from clients.models import Client, ClientComplaint
from reports.api.serializers import ReportSerializer
from reports.models import Report
from secretary.models import Secretary

User = get_user_model()



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_hr_dashboard(request):
    payload = {}
    data = {}
    errors = {}

    client_distribution = []
    recent_complaints = []
    recent_reports = []
    recent_clients = []

    secretary_id = request.query_params.get('secretary_id', None)

    if not secretary_id:
        errors['secretary_id'] = ["Secretary id required"]

    #try:
    #    secretary = Secretary.objects.get(secretary_id=secretary_id)
    #except:
    #    errors['secretary_id'] = ['Secretary does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    _recent_clients = Client.objects.all().order_by("-created_at")

    clients_serializer = ClientDetailsSerializer(_recent_clients, many=True)
    if clients_serializer:
        clients = clients_serializer.data
        recent_clients = clients

    _client_complaints = ClientComplaint.objects.all().order_by("-created_at")

    client_complaints_serializer = ClientComplaintSerializer(_client_complaints, many=True)
    if client_complaints_serializer:
        _client_complaints = client_complaints_serializer.data
        recent_complaints = _client_complaints


    reports = Report.objects.all().order_by("-created_at")
    report_serializer = ReportSerializer(reports, many=True)
    if report_serializer:
        _report_serializer = report_serializer.data
        recent_reports = _report_serializer

    data['client_distribution'] = client_distribution
    data['recent_complaints'] = recent_complaints
    data['recent_reports'] = recent_reports
    data['recent_clients'] = recent_clients


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

