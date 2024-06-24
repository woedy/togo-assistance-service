
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
from billing.api.serializers import AllClientPaymentsSerializer, ClientPaymentDetailsSerializer
from billing.models import ClientPayment
from bookings.models import Booking
from clients.api.serializers import AllClientsSerializer, ClientDetailsSerializer, AllClientComplaintsSerializer, \
    ClientComplaintDetailSerializer

from clients.models import Client, ClientComplaint

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_payment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        amount = request.data.get('amount', "")
        payment_type = request.data.get('payment_type', "")
        payment_method = request.data.get('payment_method', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not amount:
            errors['amount'] = ['Amount is required.']

        if not payment_type:
            errors['payment_type'] = ['Payment Type is required.']

        if not payment_method:
            errors['payment_method'] = ['Payment Method is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_payment = ClientPayment.objects.create(
            booking=booking,
            payment_method=payment_method,
            payment_type=payment_type,
            amount=amount,

        )


        data["payment_id"] = new_payment.payment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_client_payments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payments = ClientPayment.objects.all().filter(is_archived=False)


    if search_query:
        all_payments = all_payments.filter(
            Q(booking__booking_id__icontains=search_query) |
            Q(payment_type__icontains=search_query) |
            Q(payment_method__icontains=search_query)
        )


    paginator = Paginator(all_payments, page_size)

    try:
        paginated_client_payments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_client_payments = paginator.page(1)
    except EmptyPage:
        paginated_client_payments = paginator.page(paginator.num_pages)

    all_client_payments_serializer = AllClientPaymentsSerializer(paginated_client_payments, many=True)


    data['client_payments'] = all_client_payments_serializer.data
    data['pagination'] = {
        'page_number': paginated_client_payments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_client_payments.next_page_number() if paginated_client_payments.has_next() else None,
        'previous': paginated_client_payments.previous_page_number() if paginated_client_payments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_client_payment_details_view(request):
    payload = {}
    data = {}
    errors = {}

    payment_id = request.query_params.get('payment_id', None)

    if not payment_id:
        errors['payment_id'] = ["Payment id required"]

    try:
        payment = ClientPayment.objects.get(payment_id=payment_id)
    except:
        errors['payment_id'] = ['Payment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    client_payment_serializer = ClientPaymentDetailsSerializer(payment, many=False)
    if client_payment_serializer:
        client_payment = client_payment_serializer.data


    payload['message'] = "Successful"
    payload['data'] = client_payment

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_client_payment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payment_id = request.data.get('payment_id', "")
        booking_id = request.data.get('booking_id', "")
        amount = request.data.get('amount', "")
        payment_type = request.data.get('payment_type', "")
        payment_method = request.data.get('payment_method', "")


        if not payment_id:
            errors['payment_id'] = ['Payment ID is required.']

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not amount:
            errors['amount'] = ['Amount is required.']

        if not payment_type:
            errors['payment_type'] = ['Payment Type is required.']

        if not payment_method:
            errors['payment_method'] = ['Payment Method is required.']

        try:
            payment = ClientPayment.objects.get(payment_id=payment_id)
        except:
            errors['payment_id'] = ['Payment does not exist.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        payment.booking = booking
        payment.payment_method = payment_method
        payment.payment_type = payment_type
        payment.amount = amount
        payment.save()


        data["payment_id"] = payment.payment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_client_payment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payment_id = request.data.get('payment_id', "")

        if not payment_id:
            errors['payment_id'] = ['Payment ID is required.']

        try:
            payment = ClientPayment.objects.get(payment_id=payment_id)
        except:
            errors['payment_id'] = ['Payment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payment.is_archived = True
        payment.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_client_payment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payment_id = request.data.get('payment_id', "")

        if not payment_id:
            errors['payment_id'] = ['Payment ID is required.']

        try:
            payment = ClientPayment.objects.get(payment_id=payment_id)
        except:
            errors['payment_id'] = ['Payment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payment.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_client_payment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payment_id = request.data.get('payment_id', "")

        if not payment_id:
            errors['payment_id'] = ['Payment ID is required.']

        try:
            payment = ClientPayment.objects.get(payment_id=payment_id)
        except:
            errors['payment_id'] = ['Payment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payment.is_archived = False
        payment.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)












@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_client_payments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payments = ClientPayment.objects.all().filter(is_archived=True)


    if search_query:
        all_payments = all_payments.filter(
            Q(booking__booking_id__icontains=search_query) |
            Q(payment_type__icontains=search_query) |
            Q(payment_method__icontains=search_query)
        )


    paginator = Paginator(all_payments, page_size)

    try:
        paginated_client_payments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_client_payments = paginator.page(1)
    except EmptyPage:
        paginated_client_payments = paginator.page(paginator.num_pages)

    all_client_payments_serializer = AllClientPaymentsSerializer(paginated_client_payments, many=True)


    data['client_payments'] = all_client_payments_serializer.data
    data['pagination'] = {
        'page_number': paginated_client_payments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_client_payments.next_page_number() if paginated_client_payments.has_next() else None,
        'previous': paginated_client_payments.previous_page_number() if paginated_client_payments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)
