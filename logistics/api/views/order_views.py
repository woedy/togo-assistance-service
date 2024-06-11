
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email
from logistics.api.serializers import AllOrderSerializer, OrderDetailsSerializer
from logistics.models import Order, Supplier

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_order(request):
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
            errors['supplier_id'] = ['Supplier is required.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_order = Order.objects.create(
            status='Pending',
            supplier=supplier
        )

        data["order_id"] = new_order.order_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_orders_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_orders = Order.objects.all().filter(is_archived=False)


    if search_query:
        all_orders = all_orders.filter(
            Q(status__icontains=search_query) |
            Q(supplier__name__icontains=search_query)
        )


    paginator = Paginator(all_orders, page_size)

    try:
        paginated_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    all_orders_serializer = AllOrderSerializer(paginated_orders, many=True)


    data['orders'] = all_orders_serializer.data
    data['pagination'] = {
        'page_number': paginated_orders.number,
        'total_pages': paginator.num_pages,
        'next': paginated_orders.next_page_number() if paginated_orders.has_next() else None,
        'previous': paginated_orders.previous_page_number() if paginated_orders.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_order_details_view(request):
    payload = {}
    data = {}
    errors = {}

    order_id = request.query_params.get('order_id', None)

    if not order_id:
        errors['order_id'] = ["Order id required"]

    try:
        order = Order.objects.get(order_id=order_id)
    except:
        errors['order_id'] = ['Order does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    order_serializer = OrderDetailsSerializer(order, many=False)
    if order_serializer:
        order = order_serializer.data


    payload['message'] = "Successful"
    payload['data'] = order

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")
        supplier_id = request.data.get('supplier_id', "")
        status = request.data.get('status', "")

        if not status:
            errors['status'] = ['Status is required.']

        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        if not supplier_id:
            errors['supplier_id'] = ['Supplier ID is required.']

        try:
            supplier = Supplier.objects.get(supplier_id=supplier_id)
        except:
            errors['supplier_id'] = ['Supplier does not exist.']

        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order.name = status
        order.supplier = supplier
        order.save()

        data["order_id"] = order.order_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")

        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order.is_archived = True
        order.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")

        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        order_id = request.data.get('order_id', "")

        if not order_id:
            errors['order_id'] = ['Order ID is required.']

        try:
            order = Order.objects.get(order_id=order_id)
        except:
            errors['order_id'] = ['Order does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        order.is_archived = False
        order.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_orders_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_orders = Order.objects.all().filter(is_archived=True)


    if search_query:
        all_orders = all_orders.filter(
            Q(status__icontains=search_query) |
            Q(supplier__name__icontains=search_query)
        )




    paginator = Paginator(all_orders, page_size)

    try:
        paginated_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_orders = paginator.page(1)
    except EmptyPage:
        paginated_orders = paginator.page(paginator.num_pages)

    all_orders_serializer = AllOrderSerializer(paginated_orders, many=True)


    data['orders'] = all_orders_serializer.data
    data['pagination'] = {
        'page_number': paginated_orders.number,
        'total_pages': paginator.num_pages,
        'next': paginated_orders.next_page_number() if paginated_orders.has_next() else None,
        'previous': paginated_orders.previous_page_number() if paginated_orders.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


