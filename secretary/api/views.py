
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
from secretary.api.serializers import AllLogBookSerializer
from secretary.models import Secretary, LogBook

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
def add_log_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone = request.data.get('phone', "")
        purpose = request.data.get('purpose', "")
        _status = request.data.get('status', "")
        client_id = request.data.get('client_id', "")
        contact_type = request.data.get('contact_type', "")

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not _status:
            errors['status'] = ['Status is required.']

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not purpose:
            errors['purpose'] = ['Purpose is required.']

        if not contact_type:
            errors['contact_type'] = ['Contact Type is required.']


        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_log = LogBook.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            purpose=purpose,
            status=_status,
            client=client,
            contact_type=contact_type
        )

        data['log_id'] = new_log.log_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_log_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        log_id = request.data.get('log_id', "")
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone = request.data.get('phone', "")
        purpose = request.data.get('purpose', "")
        _status = request.data.get('status', "")
        client_id = request.data.get('client_id', "")
        contact_type = request.data.get('contact_type', "")

        if not log_id:
            errors['log_id'] = ['Log ID is required.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not _status:
            errors['status'] = ['Status is required.']

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not purpose:
            errors['purpose'] = ['Purpose is required.']

        if not contact_type:
            errors['contact_type'] = ['Contact Type is required.']


        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        try:
            log = LogBook.objects.get(log_id=log_id)
        except:
            errors['log_id'] = ['Log does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        log.first_name=first_name
        log.last_name=last_name
        log.phone=phone
        log.purpose=purpose
        log.status=status
        log.client=client
        log.contact_type=contact_type
        log.save()

        data['log_id'] = log.log_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_logs_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_logs = LogBook.objects.all().filter(is_archived=False)


    if search_query:
        all_logs = all_logs.filter(
            Q(log_id__icontains=search_query)
        )


    paginator = Paginator(all_logs, page_size)

    try:
        paginated_logs = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_logs = paginator.page(1)
    except EmptyPage:
        paginated_logs = paginator.page(paginator.num_pages)

    all_log_serializer = AllLogBookSerializer(paginated_logs, many=True)


    data['logs'] = all_log_serializer.data
    data['pagination'] = {
        'page_number': paginated_logs.number,
        'total_pages': paginator.num_pages,
        'next': paginated_logs.next_page_number() if paginated_logs.has_next() else None,
        'previous': paginated_logs.previous_page_number() if paginated_logs.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_log(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        log_id = request.data.get('log_id', "")

        if not log_id:
            errors['log_id'] = ['Log ID is required.']

        try:
            log = LogBook.objects.get(log_id=log_id)
        except:
            errors['log_id'] = ['Log does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        log.is_archived = True
        log.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_log(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        log_id = request.data.get('log_id', "")

        if not log_id:
            errors['log_id'] = ['Log ID is required.']

        try:
            log = LogBook.objects.get(log_id=log_id)
        except:
            errors['log'] = ['log does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        log.is_archived = False
        log.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_log(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        log_id = request.data.get('log_id', "")

        if not log_id:
            errors['log_id'] = ['Log ID is required.']

        try:
            log = LogBook.objects.get(log_id=log_id)
        except:
            errors['log_id'] = ['Log does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        log.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_log_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_logs = LogBook.objects.all().filter(is_archived=True)


    if search_query:
        all_logs = all_logs.filter(
            Q(log_id__icontains=search_query)
        )


    paginator = Paginator(all_logs, page_size)

    try:
        paginated_logs = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_logs = paginator.page(1)
    except EmptyPage:
        paginated_logs = paginator.page(paginator.num_pages)

    all_log_serializer = AllLogBookSerializer(paginated_logs, many=True)


    data['logs'] = all_log_serializer.data
    data['pagination'] = {
        'page_number': paginated_logs.number,
        'total_pages': paginator.num_pages,
        'next': paginated_logs.next_page_number() if paginated_logs.has_next() else None,
        'previous': paginated_logs.previous_page_number() if paginated_logs.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


