
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
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
from logistics.models import Supplier

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_supplier(request):
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


        new_supplier = Supplier.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            address=address
        )



        data["supplier_id"] = new_supplier.supplier_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_supplier_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_suppliers = Supplier.objects.all().filter(is_archived=False)


    if search_query:
        all_suppliers = all_suppliers.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email_number__icontains=search_query) |
            Q(address_number__icontains=search_query)
        )


    paginator = Paginator(all_suppliers, page_size)

    try:
        paginated_suppliers = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_suppliers = paginator.page(1)
    except EmptyPage:
        paginated_suppliers = paginator.page(paginator.num_pages)

    all_suppliers_serializer = AllClientsSerializer(paginated_suppliers, many=True)


    data['suppliers'] = all_suppliers_serializer.data
    data['pagination'] = {
        'page_number': paginated_suppliers.number,
        'total_pages': paginator.num_pages,
        'next': paginated_suppliers.next_page_number() if paginated_suppliers.has_next() else None,
        'previous': paginated_suppliers.previous_page_number() if paginated_suppliers.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_suppliers_details_view(request):
    payload = {}
    data = {}
    errors = {}

    supplier_id = request.query_params.get('supplier_id', None)

    if not supplier_id:
        errors['supplier_id'] = ["Supplier id required"]

    try:
        supplier = Supplier.objects.get(supplier_id=supplier_id)
    except:
        errors['supplier_id'] = ['Supplier does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    supplier_serializer = SupplierDetailsSerializer(supplier, many=False)
    if supplier_serializer:
        supplier = supplier_serializer.data


    payload['message'] = "Successful"
    payload['data'] = supplier

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_supplier(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        supplier_id = request.data.get('supplier_id', "")

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
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']


    if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        client_profile.user.first_name = first_name
        client_profile.company_name = company_name
        client_profile.user.last_name = last_name
        client_profile.user.phone = phone
        client_profile.user.save()

        client_profile.gender = gender
        client_profile.save()

        data["user_id"] = client_profile.user.user_id
        data["email"] = client_profile.user.email
        data["company_name"] = client_profile.company_name
        data["first_name"] = client_profile.user.first_name
        data["last_name"] = client_profile.user.last_name
        data["purpose"] = client_profile.purpose
        data["gender"] = client_profile.gender

        new_activity = AllActivity.objects.create(
            user=client_profile.user,
            subject="Profile Edited",
            body=client_profile.user.email + " Just edited their account."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_client(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        try:
            user = User.objects.get(user_id=client.user.user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = True
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account Archived",
            body=user.email + " account archived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_client(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        try:
            user = User.objects.get(user_id=client.user.user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_client(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        try:
            user = User.objects.get(user_id=client.user.user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = False
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account UnArchived",
            body=user.email + " account archived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_clients_view2222(request):
    payload = {}
    data = {}
    errors = {}

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    all_clients = Client.objects.all().filter(user__is_archived=True)

    all_clients_serializer = AllClientsSerializer(all_clients, many=True)
    if all_clients_serializer:
        _all_clients = all_clients_serializer.data

    payload['message'] = "Successful"
    payload['data'] = _all_clients


    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_clients_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_clients = Client.objects.all().filter(user__is_archived=True)


    if search_query:
        all_clients = all_clients.filter(
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__department__icontains=search_query) |
            Q(user__gender__icontains=search_query) |
            Q(user__dob__icontains=search_query) |
            Q(user__marital_status__icontains=search_query) |
            Q(user__phone__icontains=search_query) |
            Q(user__country__icontains=search_query) |
            Q(user__language__icontains=search_query) |
            Q(user__location_name__icontains=search_query)
        )


    paginator = Paginator(all_clients, page_size)

    try:
        paginated_clients = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_clients = paginator.page(1)
    except EmptyPage:
        paginated_clients = paginator.page(paginator.num_pages)

    all_clients_serializer = AllClientsSerializer(paginated_clients, many=True)


    data['clients'] = all_clients_serializer.data
    data['pagination'] = {
        'page_number': paginated_clients.number,
        'total_pages': paginator.num_pages,
        'next': paginated_clients.next_page_number() if paginated_clients.has_next() else None,
        'previous': paginated_clients.previous_page_number() if paginated_clients.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_complaint(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        title = request.data.get('title', "")
        note = request.data.get('note', "")

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not title:
            errors['title'] = ['Title is required.']

        if not note:
            errors['note'] = ['Note is required.']


        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_complaint = ClientComplaint.objects.create(
            client=client,
            title=title,
            note=note,

        )

        data["complaint_id"] = new_complaint.id

        new_activity = AllActivity.objects.create(
            user=client.user,
            subject="New Client Complaint",
            body=client.user.email + " Added a new complaint."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)
