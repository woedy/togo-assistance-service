
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email
from logistics.api.serializers import AllInventorySerializer, InventoryDetailsSerializer

from logistics.models import Inventory, Equipment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_inventory(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        equipment_id = request.data.get('equipment_id', "")
        quantity = request.data.get('quantity', "")



        if not equipment_id:
            errors['equipment_id'] = ['Equipment is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_inventory = Inventory.objects.create(
            equipment=equipment,
            quantity=quantity,
        )



        data["inventory_id"] = new_inventory.inventory_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_inventorys_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_inventorys = Inventory.objects.all().filter(is_archived=False)


    if search_query:
        all_inventorys = all_inventorys.filter(
            Q(equipment_name__icontains=search_query) |
            Q(quantity__icontains=search_query)
        )


    paginator = Paginator(all_inventorys, page_size)

    try:
        paginated_inventorys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_inventorys = paginator.page(1)
    except EmptyPage:
        paginated_inventorys = paginator.page(paginator.num_pages)

    all_inventorys_serializer = AllInventorySerializer(paginated_inventorys, many=True)


    data['inventorys'] = all_inventorys_serializer.data
    data['pagination'] = {
        'page_number': paginated_inventorys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_inventorys.next_page_number() if paginated_inventorys.has_next() else None,
        'previous': paginated_inventorys.previous_page_number() if paginated_inventorys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_inventory_details_view(request):
    payload = {}
    data = {}
    errors = {}

    inventory_id = request.query_params.get('inventory_id', None)

    if not inventory_id:
        errors['inventory_id'] = ["Inventory id required"]

    try:
        inventory = Inventory.objects.get(inventory_id=inventory_id)
    except:
        errors['inventory_id'] = ['Inventory does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    inventory_serializer = InventoryDetailsSerializer(inventory, many=False)
    if inventory_serializer:
        inventory = inventory_serializer.data


    payload['message'] = "Successful"
    payload['data'] = inventory

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_inventory(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        inventory_id = request.data.get('inventory_id', "")
        equipment_id = request.data.get('equipment_id', "")
        quantity = request.data.get('quantity', "")

        if not equipment_id:
            errors['equipment_id'] = ['Equipment is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']

        try:
            inventory = Inventory.objects.get(inventory_id=inventory_id)
        except:
            errors['inventory_id'] = ['Inventory does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        inventory.equipment = equipment
        inventory.quantity = quantity
        inventory.save()

        data["inventory_id"] = inventory.inventory_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_inventory(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        inventory_id = request.data.get('inventory_id', "")

        if not inventory_id:
            errors['inventory_id'] = ['Inventory ID is required.']

        try:
            inventory = Inventory.objects.get(inventory_id=inventory_id)
        except:
            errors['inventory_id'] = ['Inventory does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        inventory.is_archived = True
        inventory.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_inventory(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        inventory_id = request.data.get('inventory_id', "")

        if not inventory_id:
            errors['inventory_id'] = ['Inventory ID is required.']

        try:
            inventory = Inventory.objects.get(inventory_id=inventory_id)
        except:
            errors['inventory_id'] = ['Inventory does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        inventory.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_inventory(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        inventory_id = request.data.get('inventory_id', "")

        if not inventory_id:
            errors['inventory_id'] = ['Inventory ID is required.']

        try:
            inventory = Inventory.objects.get(inventory_id=inventory_id)
        except:
            errors['inventory_id'] = ['Inventory does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        inventory.is_archived = False
        inventory.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_inventorys_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_inventorys = Inventory.objects.all().filter(is_archived=True)


    if search_query:
        all_inventorys = all_inventorys.filter(
            Q(equipment__name__icontains=search_query) |
            Q(quantity__icontains=search_query)
        )

    paginator = Paginator(all_inventorys, page_size)

    try:
        paginated_inventorys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_inventorys = paginator.page(1)
    except EmptyPage:
        paginated_inventorys = paginator.page(paginator.num_pages)

    all_inventorys_serializer = AllInventorySerializer(paginated_inventorys, many=True)


    data['inventorys'] = all_inventorys_serializer.data
    data['pagination'] = {
        'page_number': paginated_inventorys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_inventorys.next_page_number() if paginated_inventorys.has_next() else None,
        'previous': paginated_inventorys.previous_page_number() if paginated_inventorys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


