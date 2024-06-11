
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email
from logistics.api.serializers import EquipmentDetailsSerializer, AllEquipmentSerializer
from logistics.models import Equipment, Category, Supplier

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_equipment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        category_id = request.data.get('category_id', "")
        supplier_id = request.data.get('supplier_id', "")
        name = request.data.get('name', "")
        description = request.data.get('description', "")
        price = request.data.get('price', "")
        serial_number = request.data.get('serial_number', "")
        purchase_date = request.data.get('purchase_date', "")

        if not name:
            errors['name'] = ['Name is required.']

        if not category_id:
            errors['category_id'] = ['Category ID is required.']

        if not supplier_id:
            errors['supplier_id'] = ['Supplier ID is required.']

        elif check_equipment_name_exist(name):
            errors['name'] = ['Equipment name already exists in our database.']


        if not serial_number:
            errors['serial_number'] = ['Serial Number is required.']

        if not price:
            errors['price'] = ['Price is required.']

        try:
            category = Category.objects.get(category_id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']

        try:
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_equipment = Equipment.objects.create(
            name=name,
            category=category,
            supplier=supplier,
            description=description,
            price=price,
            serial_number=serial_number,
            purchase_date=purchase_date,
        )



        data["equipment_id"] = new_equipment.equipment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


def check_equipment_name_exist(name):
    qs = Equipment.objects.filter(name=name)
    if qs.exists():
        return True
    else:
        return False

@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_equipment_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_equipments = Equipment.objects.all().filter(is_archived=False)


    if search_query:
        all_equipments = all_equipments.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(supplier__name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(purchase_date__icontains=search_query)
        )


    paginator = Paginator(all_equipments, page_size)

    try:
        paginated_equipments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_equipments = paginator.page(1)
    except EmptyPage:
        paginated_equipments = paginator.page(paginator.num_pages)

    all_equipments_serializer = AllEquipmentSerializer(paginated_equipments, many=True)


    data['equipments'] = all_equipments_serializer.data
    data['pagination'] = {
        'page_number': paginated_equipments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_equipments.next_page_number() if paginated_equipments.has_next() else None,
        'previous': paginated_equipments.previous_page_number() if paginated_equipments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_equipment_details_view(request):
    payload = {}
    data = {}
    errors = {}

    equipment_id = request.query_params.get('equipment_id', None)

    if not equipment_id:
        errors['equipment_id'] = ["Equipment id required"]

    try:
        equipment = Equipment.objects.get(equipment_id=equipment_id)
    except:
        errors['equipment_id'] = ['Equipment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    equipment_serializer = EquipmentDetailsSerializer(equipment, many=False)
    if equipment_serializer:
        equipment = equipment_serializer.data


    payload['message'] = "Successful"
    payload['data'] = equipment

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_equipment(request):
    payload = {}
    data = {}
    errors = {}


    if request.method == 'POST':
        equipment_id = request.data.get('equipment_id', "")
        category_id = request.data.get('category_id', "")
        supplier_id = request.data.get('supplier_id', "")
        name = request.data.get('name', "")
        description = request.data.get('description', "")
        price = request.data.get('price', "")
        serial_number = request.data.get('serial_number', "")
        purchase_date = request.data.get('purchase_date', "")

        if not name:
            errors['name'] = ['Name is required.']

        if not category_id:
            errors['category_id'] = ['Category ID is required.']

        if not supplier_id:
            errors['supplier_id'] = ['Supplier ID is required.']

        elif check_equipment_name_exist(name):
            errors['name'] = ['Equipment name already exists in our database.']


        if not serial_number:
            errors['serial_number'] = ['Serial Number is required.']

        if not price:
            errors['price'] = ['Price is required.']

        try:
            category = Category.objects.get(category_id=category_id)
        except:
            errors['category_id'] = ['Category does not exist.']

        try:
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']



        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        equipment.name = name
        equipment.category = category
        equipment.supplier = supplier
        equipment.description = description
        equipment.price = price
        equipment.serial_number = serial_number
        equipment.purchase_date = purchase_date
        equipment.save()

        data["equipment_id"] = equipment.equipment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_equipment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        equipment_id = request.data.get('equipment_id', "")

        if not equipment_id:
            errors['equipment_id'] = ['Equipment ID is required.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        equipment.is_archived = True
        equipment.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_equipment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        equipment_id = request.data.get('equipment_id', "")

        if not equipment_id:
            errors['equipment_id'] = ['Equipment ID is required.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        equipment.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_equipment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        equipment_id = request.data.get('equipment_id', "")

        if not equipment_id:
            errors['equipment_id'] = ['Equipment ID is required.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        equipment.is_archived = False
        equipment.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_equipments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_equipments = Equipment.objects.all().filter(is_archived=True)


    if search_query:
        all_equipments = all_equipments.filter(
            Q(name__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(supplier__name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(price__icontains=search_query) |
            Q(serial_number__icontains=search_query) |
            Q(purchase_date__icontains=search_query)

        )




    paginator = Paginator(all_equipments, page_size)

    try:
        paginated_equipments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_equipments = paginator.page(1)
    except EmptyPage:
        paginated_equipments = paginator.page(paginator.num_pages)

    all_equipments_serializer = AllEquipmentSerializer(paginated_equipments, many=True)


    data['equipments'] = all_equipments_serializer.data
    data['pagination'] = {
        'page_number': paginated_equipments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_equipments.next_page_number() if paginated_equipments.has_next() else None,
        'previous': paginated_equipments.previous_page_number() if paginated_equipments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


