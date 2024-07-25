
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
from bookings.api.serializers import PostOrderDetailsSerializer, AllPostOrdersSerializer
from clients.api.serializers import AllClientsSerializer, ClientDetailsSerializer, AllClientComplaintsSerializer, \
    ClientComplaintDetailSerializer

from clients.models import Client, ClientComplaint
from post_sites.models import ClientPostSite, PostOrder

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_post_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_id = request.data.get('site_id', "")
        subject = request.data.get('subject', "")
        description = request.data.get('description', "")


        if not site_id:
            errors['site_id'] = ['Post Site ID is required.']

        if not subject:
            errors['subject'] = ['Subject is required.']

        if not description:
            errors['description'] = ['Description is required.']

        try:
            post_site = ClientPostSite.objects.get(site_id=site_id)
        except:
            errors['site_id'] = ['Post Site does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        post_order = PostOrder.objects.create(
            post_site=post_site,
            subject=subject,
            description=description,
        )

        data["post_order_id"] = post_order.post_order_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_post_orders_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_post_orders = PostOrder.objects.all().filter(is_archived=False)


    if search_query:
        all_post_orders = all_post_orders.filter(
            Q(post_order_id__icontains=search_query) |
            Q(subject__icontains=search_query)

        )


    paginator = Paginator(all_post_orders, page_size)

    try:
        paginated_post_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_post_orders = paginator.page(1)
    except EmptyPage:
        paginated_post_orders = paginator.page(paginator.num_pages)

    all_post_orders_serializer = AllPostOrdersSerializer(paginated_post_orders, many=True)


    data['post_orders'] = all_post_orders_serializer.data
    data['pagination'] = {
        'page_number': paginated_post_orders.number,
        'total_pages': paginator.num_pages,
        'next': paginated_post_orders.next_page_number() if paginated_post_orders.has_next() else None,
        'previous': paginated_post_orders.previous_page_number() if paginated_post_orders.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_post_order_details_view(request):
    payload = {}
    data = {}
    errors = {}

    post_order_id = request.query_params.get('post_order_id', None)

    if not post_order_id:
        errors['post_order_id'] = ["Post Order id required"]

    try:
        post_order = PostOrder.objects.get(post_order_id=post_order_id)
    except:
        errors['post_order_id'] = ['Post Order does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    post_order_serializer = PostOrderDetailsSerializer(post_order, many=False)
    if post_order_serializer:
        post_order = post_order_serializer.data


    payload['message'] = "Successful"
    payload['data'] = post_order

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_post_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        post_order_id = request.data.get('post_order_id', "")
        site_id = request.data.get('site_id', "")
        subject = request.data.get('subject', "")
        description = request.data.get('description', "")

        if not post_order_id:
            errors['post_order_id'] = ['Post Order ID is required.']


        if not site_id:
            errors['site_id'] = ['Post Site ID is required.']

        if not subject:
            errors['subject'] = ['Subject is required.']

        if not description:
            errors['description'] = ['Description is required.']

        try:
            post_site = ClientPostSite.objects.get(site_id=site_id)
        except:
            errors['site_id'] = ['Post Site does not exist.']


        try:
            post_order = PostOrder.objects.get(post_order_id=post_order_id)
        except:
            errors['post_order_id'] = ['Post Order does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        post_order.subject = subject
        post_order.description = description
        post_order.post_site = post_site
        post_order.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_post_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        post_order_id = request.data.get('post_order_id', "")

        if not post_order_id:
            errors['post_order_id'] = ['Post Order ID is required.']

        try:
            post_order = PostOrder.objects.get(post_order_id=post_order_id)
        except:
            errors['post_order_id'] = ['Post_Order does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        post_order.is_archived = True
        post_order.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_post_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        post_order_id = request.data.get('post_order_id', "")

        if not post_order_id:
            errors['post_order_id'] = ['Post Order ID is required.']

        try:
            post_order = PostOrder.objects.get(post_order_id=post_order_id)
        except:
            errors['post_order_id'] = ['Post_Order does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        post_order.is_archived = False
        post_order.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_post_order(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        post_order_id = request.data.get('post_order_id', "")

        if not post_order_id:
            errors['post_order_id'] = ['Post Order ID is required.']

        try:
            post_order = PostOrder.objects.get(post_order_id=post_order_id)
        except:
            errors['post_order_id'] = ['Post_Order does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        post_order.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_unarchived_post_orders_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_post_orders = PostOrder.objects.all().filter(is_archived=True)


    if search_query:
        all_post_orders = all_post_orders.filter(
            Q(post_order_id__icontains=search_query) |
            Q(subject__icontains=search_query)

        )


    paginator = Paginator(all_post_orders, page_size)

    try:
        paginated_post_orders = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_post_orders = paginator.page(1)
    except EmptyPage:
        paginated_post_orders = paginator.page(paginator.num_pages)

    all_post_orders_serializer = AllPostOrdersSerializer(paginated_post_orders, many=True)


    data['post_orders'] = all_post_orders_serializer.data
    data['pagination'] = {
        'page_number': paginated_post_orders.number,
        'total_pages': paginator.num_pages,
        'next': paginated_post_orders.next_page_number() if paginated_post_orders.has_next() else None,
        'previous': paginated_post_orders.previous_page_number() if paginated_post_orders.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

