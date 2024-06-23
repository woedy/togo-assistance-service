
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import Deployment, Booking
from clients.api.serializers import ClientDetailsSerializer, AllClientComplaintsSerializer

from clients.models import Client, ClientComplaint
from operations.models import Operation
from reports.api.serializers import ReportSerializer
from reports.models import Report
from secretary.models import Secretary

User = get_user_model()



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_operations_dashboard(request):
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

    client_complaints_serializer = AllClientComplaintsSerializer(_client_complaints, many=True)
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



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def update_role(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        operations_id = request.data.get('operations_id', "")
        role = request.data.get('role', "")

        if not role:
            errors['role'] = ['Role is required.']

        if not operations_id:
            errors['operations_id'] = ['Operations ID Email is required.']


        try:
            operations = Operation.objects.get(operations_id=operations_id)
        except:
            errors['operations_id'] = ['Operations does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        operations.role = role
        operations.save()


        data["operations_id"] = operations.operations_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

