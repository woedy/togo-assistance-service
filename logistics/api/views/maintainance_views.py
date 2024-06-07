
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email
from logistics.models import Maintenance

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_maintenance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()
        name = request.data.get('name', "")
        phone_number = request.data.get('phone_number', "")
        address = request.data.get('address', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']

        if not name:
            errors['name'] = ['Name is required.']

        if not phone_number:
            errors['phone_number'] = ['Phone is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_maintenance = Maintenance.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            address=address
        )



        data["maintenance_id"] = new_maintenance.maintenance_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_maintenance_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_maintenances = Maintenance.objects.all().filter(is_archived=False)


    if search_query:
        all_maintenances = all_maintenances.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email_number__icontains=search_query) |
            Q(address_number__icontains=search_query)
        )


    paginator = Paginator(all_maintenances, page_size)

    try:
        paginated_maintenances = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_maintenances = paginator.page(1)
    except EmptyPage:
        paginated_maintenances = paginator.page(paginator.num_pages)

    all_maintenances_serializer = AllMaintenanceSerializer(paginated_maintenances, many=True)


    data['maintenances'] = all_maintenances_serializer.data
    data['pagination'] = {
        'page_number': paginated_maintenances.number,
        'total_pages': paginator.num_pages,
        'next': paginated_maintenances.next_page_number() if paginated_maintenances.has_next() else None,
        'previous': paginated_maintenances.previous_page_number() if paginated_maintenances.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_maintenance_details_view(request):
    payload = {}
    data = {}
    errors = {}

    maintenance_id = request.query_params.get('maintenance_id', None)

    if not maintenance_id:
        errors['maintenance_id'] = ["Maintenance id required"]

    try:
        maintenance = Maintenance.objects.get(maintenance_id=maintenance_id)
    except:
        errors['maintenance_id'] = ['Maintenance does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    maintenance_serializer = MaintenanceDetailsSerializer(maintenance, many=False)
    if maintenance_serializer:
        maintenance = maintenance_serializer.data


    payload['message'] = "Successful"
    payload['data'] = maintenance

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_maintenance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        maintenance_id = request.data.get('maintenance_id', "")

        email = request.data.get('email', "").lower()
        name = request.data.get('name', "")
        phone_number = request.data.get('phone_number', "")
        address = request.data.get('address', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']

        if not name:
            errors['name'] = ['Name is required.']

        if not phone_number:
            errors['phone_number'] = ['Phone is required.']

        try:
            maintenance = Maintenance.objects.get(maintenance_id=maintenance_id)
        except:
            errors['maintenance_id'] = ['Maintenance does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        maintenance.name = name
        maintenance.phone_number = phone_number
        maintenance.email = email
        maintenance.address = address
        maintenance.save()

        data["maintenance_id"] = maintenance.maintenance_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_maintenance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        maintenance_id = request.data.get('maintenance_id', "")

        if not maintenance_id:
            errors['maintenance_id'] = ['Maintenance ID is required.']

        try:
            maintenance = Maintenance.objects.get(maintenance_id=maintenance_id)
        except:
            errors['maintenance_id'] = ['Maintenance does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        maintenance.is_archived = True
        maintenance.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_maintenance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        maintenance_id = request.data.get('maintenance_id', "")

        if not maintenance_id:
            errors['maintenance_id'] = ['Maintenance ID is required.']

        try:
            maintenance = Maintenance.objects.get(maintenance_id=maintenance_id)
        except:
            errors['maintenance_id'] = ['Maintenance does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        maintenance.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_maintenance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        maintenance_id = request.data.get('maintenance_id', "")

        if not maintenance_id:
            errors['maintenance_id'] = ['Maintenance ID is required.']

        try:
            maintenance = Maintenance.objects.get(maintenance_id=maintenance_id)
        except:
            errors['maintenance_id'] = ['Maintenance does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        maintenance.is_archived = False
        maintenance.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_maintenances_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_maintenances = Maintenance.objects.all().filter(is_archived=True)


    if search_query:
        all_maintenances = all_maintenances.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email_number__icontains=search_query) |
            Q(address_number__icontains=search_query)


        )




    paginator = Paginator(all_maintenances, page_size)

    try:
        paginated_maintenances = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_maintenances = paginator.page(1)
    except EmptyPage:
        paginated_maintenances = paginator.page(paginator.num_pages)

    all_maintenances_serializer = AllMaintenanceSerializer(paginated_maintenances, many=True)


    data['maintenances'] = all_maintenances_serializer.data
    data['pagination'] = {
        'page_number': paginated_maintenances.number,
        'total_pages': paginator.num_pages,
        'next': paginated_maintenances.next_page_number() if paginated_maintenances.has_next() else None,
        'previous': paginated_maintenances.previous_page_number() if paginated_maintenances.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


