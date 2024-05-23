
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from clients.api.serializers import ClientDetailsSerializer, ClientComplaintSerializer

from clients.models import Client, ClientComplaint
from reports.api.serializers import ReportSerializer
from reports.models import Report
from secretary.api.serializers import AllWalkinLogsSerializer
from secretary.models import Secretary, WalkInLog

User = get_user_model()



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_secretary_dashboard(request):
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



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_walkin_log_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone = request.data.get('phone', "")
        purpose = request.data.get('purpose', "")
        _status = request.data.get('status', "")

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not _status:
            errors['status'] = ['Status is required.']

        if not purpose:
            errors['purpose'] = ['Purpose is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_walkin = WalkInLog.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            purpose=purpose,
            status=_status
        )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_walkins_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_walkins = WalkInLog.objects.all().filter(is_archived=False)


    if search_query:
        all_walkins = all_walkins.filter(
            Q(walk_in_id__icontains=search_query)
        )


    paginator = Paginator(all_walkins, page_size)

    try:
        paginated_walkins = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_walkins = paginator.page(1)
    except EmptyPage:
        paginated_walkins = paginator.page(paginator.num_pages)

    all_walkin_log_serializer = AllWalkinLogsSerializer(paginated_walkins, many=True)


    data['walkin_logs'] = all_walkin_log_serializer.data
    data['pagination'] = {
        'page_number': paginated_walkins.number,
        'total_pages': paginator.num_pages,
        'next': paginated_walkins.next_page_number() if paginated_walkins.has_next() else None,
        'previous': paginated_walkins.previous_page_number() if paginated_walkins.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_walkin(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        walk_in_id = request.data.get('walk_in_id', "")

        if not walk_in_id:
            errors['walk_in_id'] = ['Walkin ID is required.']

        try:
            walkin = WalkInLog.objects.get(walk_in_id=walk_in_id)
        except:
            errors['walk_in_id'] = ['Walkin does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        walkin.is_archived = True
        walkin.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_walkin(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        walk_in_id = request.data.get('walk_in_id', "")

        if not walk_in_id:
            errors['walk_in_id'] = ['Walkin ID is required.']

        try:
            walkin = WalkInLog.objects.get(walk_in_id=walk_in_id)
        except:
            errors['walkin_log_id'] = ['Walkin log does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        walkin.is_archived = False
        walkin.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_walkin(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        walk_in_id = request.data.get('walk_in_id', "")

        if not walk_in_id:
            errors['walk_in_id'] = ['Walkin ID is required.']

        try:
            walkin = WalkInLog.objects.get(walk_in_id=walk_in_id)
        except:
            errors['walk_in_id'] = ['Walkin does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        walkin.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_walkin_log_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_walkins = WalkInLog.objects.all().filter(is_archived=True)


    if search_query:
        all_walkins = all_walkins.filter(
            Q(walk_in_id__icontains=search_query)
        )


    paginator = Paginator(all_walkins, page_size)

    try:
        paginated_walkins = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_walkins = paginator.page(1)
    except EmptyPage:
        paginated_walkins = paginator.page(paginator.num_pages)

    all_walkin_log_serializer = AllWalkinLogsSerializer(paginated_walkins, many=True)


    data['walkin_logs'] = all_walkin_log_serializer.data
    data['pagination'] = {
        'page_number': paginated_walkins.number,
        'total_pages': paginator.num_pages,
        'next': paginated_walkins.next_page_number() if paginated_walkins.has_next() else None,
        'previous': paginated_walkins.previous_page_number() if paginated_walkins.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


