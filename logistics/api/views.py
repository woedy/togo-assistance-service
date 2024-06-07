
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
from logistics.api.serializers import SupplierDetailsSerializer, AllSupplierSerializer
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

    all_suppliers_serializer = AllSupplierSerializer(paginated_suppliers, many=True)


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
def get_supplier_details_view(request):
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

        supplier.name = name
        supplier.phone_number = phone_number
        supplier.email = email
        supplier.address = address
        supplier.save()

        data["supplier_id"] = supplier.supplier_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_supplier(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        supplier_id = request.data.get('supplier_id', "")

        if not supplier_id:
            errors['supplier_id'] = ['Supplier ID is required.']

        try:
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        supplier.is_archived = True
        supplier.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_supplier(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        supplier_id = request.data.get('supplier_id', "")

        if not supplier_id:
            errors['supplier_id'] = ['Supplier ID is required.']

        try:
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        supplier.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_supplier(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        supplier_id = request.data.get('supplier_id', "")

        if not supplier_id:
            errors['supplier_id'] = ['Supplier ID is required.']

        try:
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        supplier.is_archived = False
        supplier.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_suppliers_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_suppliers = Supplier.objects.all().filter(is_archived=True)


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

    all_suppliers_serializer = AllSupplierSerializer(paginated_suppliers, many=True)


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


