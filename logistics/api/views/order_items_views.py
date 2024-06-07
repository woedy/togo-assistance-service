
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from logistics.api.serializers import AllOrderItemSerializer, OrderItemDetailsSerializer
from logistics.models import OrderItem, Order, Equipment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':

        order_id = request.data.get('order_id', "")
        equipment_id = request.data.get('equipment_id', "")
        quantity = request.data.get('quantity', "")
        price = request.data.get('price', "")


        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        if not equipment_id:
            errors['equipment_id'] = ['Equipment ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        if not price:
            errors['price'] = ['Price is required.']


        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_order_item = OrderItem.objects.create(
            order=order,
            equipment=equipment,
            quantity=quantity,
            price=price
        )

        data["order_item_id"] = new_order_item.order_item_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_order_item_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_order_items = OrderItem.objects.all().filter(is_archived=False)


    if search_query:
        all_order_items = all_order_items.filter(
            Q(order_item_id__icontains=search_query)
        )


    paginator = Paginator(all_order_items, page_size)

    try:
        paginated_order_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_order_items = paginator.page(1)
    except EmptyPage:
        paginated_order_items = paginator.page(paginator.num_pages)

    all_order_items_serializer = AllOrderItemSerializer(paginated_order_items, many=True)


    data['order_items'] = all_order_items_serializer.data
    data['pagination'] = {
        'page_number': paginated_order_items.number,
        'total_pages': paginator.num_pages,
        'next': paginated_order_items.next_page_number() if paginated_order_items.has_next() else None,
        'previous': paginated_order_items.previous_page_number() if paginated_order_items.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_order_item_details_view(request):
    payload = {}
    data = {}
    errors = {}

    order_item_id = request.query_params.get('order_item_id', None)

    if not order_item_id:
        errors['order_item_id'] = ["Order Item ID required"]

    try:
        order_item = OrderItem.objects.get(order_item_id=order_item_id)
    except:
        errors['order_item_id'] = ['Order Item does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    order_item_serializer = OrderItemDetailsSerializer(order_item, many=False)
    if order_item_serializer:
        order_item = order_item_serializer.data


    payload['message'] = "Successful"
    payload['data'] = order_item

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':

        order_item_id = request.data.get('order_item_id', "")
        quantity = request.data.get('quantity', "")
        price = request.data.get('price', "")


        if not order_item_id:
            errors['order_item_id'] = ['Order item ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        if not price:
            errors['price'] = ['Price is required.']

        try:
            order_item = OrderItem.objects.get(order_item_id=order_item_id)
        except:
            errors['order_item_id'] = ['Order Item does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order_item.quantity = quantity
        order_item.price = price
        order_item.save()

        data["order_item_id"] = order_item.order_item_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id', "")

        if not order_item_id:
            errors['order_item_id'] = ['Order Item ID is required.']

        try:
            order_item = OrderItem.objects.get(order_item_id=order_item_id)
        except:
            errors['order_item_id'] = ['Order item does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order_item.is_archived = True
        order_item.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id', "")

        if not order_item_id:
            errors['order_item_id'] = ['Order item ID is required.']

        try:
            order_item = OrderItem.objects.get(order_item_id=order_item_id)
        except:
            errors['order_item_id'] = ['Order Item does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order_item.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_order_item(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_item_id = request.data.get('order_item_id', "")

        if not order_item_id:
            errors['order_item_id'] = ['Order Item ID is required.']

        try:
            order_item = OrderItem.objects.get(order_item_id=order_item_id)
        except:
            errors['order_item_id'] = ['Order Item does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order_item.is_archived = False
        order_item.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_order_items_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_order_items = OrderItem.objects.all().filter(is_archived=True)


    if search_query:
        all_order_items = all_order_items.filter(
            Q(name__icontains=search_query)


        )




    paginator = Paginator(all_order_items, page_size)

    try:
        paginated_order_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_order_items = paginator.page(1)
    except EmptyPage:
        paginated_order_items = paginator.page(paginator.num_pages)

    all_order_items_serializer = AllOrderItemSerializer(paginated_order_items, many=True)


    data['order_items'] = all_order_items_serializer.data
    data['pagination'] = {
        'page_number': paginated_order_items.number,
        'total_pages': paginator.num_pages,
        'next': paginated_order_items.next_page_number() if paginated_order_items.has_next() else None,
        'previous': paginated_order_items.previous_page_number() if paginated_order_items.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


