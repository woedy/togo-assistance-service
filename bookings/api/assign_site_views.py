from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import BookedGuard, Booking
from security_team.models import SecurityGuard


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def assign_guard(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        slot_id = request.data.get('slot_id', "")
        time = request.data.get('time', "")
        booking_id = request.data.get('booking_id', "")




        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not time:
            errors['time'] = ['Time is required.']

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            guard = SecurityGuard.objects.get(gaurd_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        ###### Check if guard ia already assigned to booking

        booked_guard = BookedGuard.objects.filter(booking=booking).filter(guard=guard)

        if booked_guard.exist:
            errors['booking_id'] = ['Guard is already assigned.']
        else:
            assigned = BookedGuard.objects.create(
                booking=booking,
                guard=guard
            )

            ## Set Guard availabilty to occupied





        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unassign_guard(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        slot_id = request.data.get('slot_id', "")
        time = request.data.get('time', "")
        booking_id = request.data.get('booking_id', "")




        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not time:
            errors['time'] = ['Time is required.']

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            guard = SecurityGuard.objects.get(gaurd_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        ###### Check if guard ia already assigned to booking

        booked_guard = BookedGuard.objects.filter(booking=booking).filter(guard=guard)

        if booked_guard.exist:
            booked_guard.first()
            booked_guard.delete()
        else:
            errors['booking_id'] = ['Guard is already unassigned.']

            ## Set Guard availabilty to unoccupied





        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def re_assign_guard(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        booking_id = request.data.get('booking_id', "")
        new_booking_id = request.data.get('new_booking_id', "")




        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']



        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']



        if not new_booking_id:
            errors['new_booking_id'] = ['New Booking ID is required.']

        try:
            guard = SecurityGuard.objects.get(gaurd_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        try:
            new_booking = Booking.objects.get(booking_id=new_booking_id)
        except:
            errors['new_booking_id'] = ['New Booking does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        ###### Check if guard ia already assigned to booking

        booked_guard = BookedGuard.objects.filter(booking=booking).filter(guard=guard)

        if booked_guard.exist:
            booked_guard.first()
            booked_guard.delete()


            assigned = BookedGuard.objects.create(
                booking=new_booking,
                guard=guard
            )


        else:
            errors['booking_id'] = ['Guard is already unassigned.']





        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)
