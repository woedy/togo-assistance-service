from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import Booking




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_estimate_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        item = request.data.get('item', "")
        quantity = request.data.get('quantity', "")
        tax = request.data.get('tax', "")
        amount = request.data.get('amount', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not item:
            errors['item'] = ['Item required.']

        if not quantity:
            errors['quantity'] = ['Item quantity required.']


        if not tax:
            errors['tax'] = ['Tax required.']

        if not amount:
            errors['amount'] = ['Amount required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_estimate = Estimate.objects.create(
                booking=booking,
                item=item,
                quantity=quantity,
                tax=tax,
                client=booking.client,
                amount=amount,
            )




        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_contract_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        file = request.data.get('item', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not file:
            errors['file'] = ['File required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_contract = Contract.objects.create(
                booking=booking,
                file=file,
            )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

