from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.api.serializers import AllBookedGuardsSerializer
from bookings.models import BookedGuard, Booking
from security_team.models import SecurityGuard, TimeSlot


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
        _time = request.data.get('time', "")
        booking_id = request.data.get('booking_id', "")





        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not _time:
            errors['time'] = ['Time is required.']

        if not _time:
            errors['time'] = ['Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(_time) < 8:
                _time += ':00'

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)


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

        booked_guard = BookedGuard.objects.filter(booking=booking).filter(guard=guard).first()



        if booked_guard is not None:
            errors['booking_id'] = ['Guard is already assigned.']

            if errors:
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        else:
            assigned = BookedGuard.objects.create(
                booking=booking,
                guard=guard
            )

            ## Set Guard availabilty to occupied

            slot_times = TimeSlot.objects.filter(guard_slot__id=slot_id)


            for time in slot_times:
                print('###########################')
                print(time.time)
                print(_time)
                if str(time.time) == str(_time):

                    print("################")
                    print("The time is in the database")
                    if time.occupied:
                        errors['slot_time'] = ['Slot time is already occupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                    elif not time.occupied:
                        time.occupied = True
                        time.occupant = booking.client
                        time.booking_id = booking.id
                        time.save()





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
        _time = request.data.get('time', "")
        booking_id = request.data.get('booking_id', "")




        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not _time:
            errors['time'] = ['Time is required.']

        if not _time:
            errors['time'] = ['Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(_time) < 8:
                _time += ':00'

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
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

        booked_guard = BookedGuard.objects.filter(booking=booking).filter(guard=guard).first()

        if booked_guard:
            booked_guard.delete()

            ## Set Guard availabilty to unoccupied

            slot_times = TimeSlot.objects.filter(guard_slot__id=slot_id)


            for time in slot_times:
                print('###########################')
                print(time.time)
                print(_time)
                if str(time.time) == str(_time):

                    print("################")
                    print("The time is in the database")
                    if time.occupied:

                        time.occupied = False
                        time.occupant = None
                        time.booking_id = 0
                        time.save()

                    elif not time.occupied:

                        errors['slot_time'] = ['Slot time is already unoccupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)





        else:
            errors['booking_id'] = ['Guard is already unassigned.']


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
        slot_id = request.data.get('slot_id', "")
        _time = request.data.get('time', "")
        old_booking_id = request.data.get('old_booking_id', "")
        new_booking_id = request.data.get('new_booking_id', "")





        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not slot_id:
            errors['slot_id'] = ['Slot ID is required.']

        if not _time:
            errors['time'] = ['Time is required.']

        if not _time:
            errors['time'] = ['Slot time is required.']
        else:
            # Ensure the time is in the format "HH:MM:SS"
            if len(_time) < 8:
                _time += ':00'

        if not old_booking_id:
            errors['old_booking_id'] = ['Old Booking ID is required.']

        if not new_booking_id:
            errors['new_booking_id'] = ['New Booking ID is required.']

        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)


        except:
            errors['guard_id'] = ['Guard does not exist.']


        try:
            old_booking = Booking.objects.get(booking_id=old_booking_id)
        except:
            errors['old_booking_id'] = ['Old Booking does not exist.']


        try:
            new_booking = Booking.objects.get(booking_id=new_booking_id)
        except:
            errors['new_booking_id'] = ['New Booking does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        old_booked_guard = BookedGuard.objects.filter(booking=old_booking).filter(guard=guard).first()



        if old_booked_guard:
            old_booked_guard.delete()

            ## Set Guard availabilty to unoccupied

            slot_times = TimeSlot.objects.filter(guard_slot__id=slot_id)


            for time in slot_times:
                print('###########################')
                print(time.time)
                print(_time)
                if str(time.time) == str(_time):

                    print("################")
                    print("The time is in the database")
                    if time.occupied:

                        time.occupied = False
                        time.occupant = None
                        time.booking_id = 0
                        time.save()

                    elif not time.occupied:

                        errors['slot_time'] = ['Slot time is already unoccupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_booked_guard = BookedGuard.objects.filter(booking=new_booking).filter(guard=guard).first()

        if new_booked_guard is not None:
            errors['new_booking_id'] = ['Guard is already assigned.']

            if errors:
                payload['message'] = "Errors"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        else:
            assigned = BookedGuard.objects.create(
                booking=new_booking,
                guard=guard
            )

            ## Set Guard availabilty to occupied

            slot_times = TimeSlot.objects.filter(guard_slot__id=slot_id)


            for time in slot_times:
                print('###########################')
                print(time.time)
                print(_time)
                if str(time.time) == str(_time):

                    print("################")
                    print("The time is in the database")
                    if time.occupied:
                        errors['slot_time'] = ['Slot time is already occupied.']
                        payload['message'] = "Errors"
                        payload['errors'] = errors
                        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
                    elif not time.occupied:
                        time.occupied = True
                        time.occupant = new_booking.client
                        time.booking_id = new_booking.id
                        time.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_assigned_guards(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    filter_assignment = request.query_params.get('filter_assignment', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_assignments = BookedGuard.objects.all()


    if search_query:
        all_assignments = all_assignments.filter(
            Q(booking_booking_id__icontains=search_query) |
            Q(guard_guard_id__icontains=search_query)

        )

    if filter_assignment:
        all_assignments = all_assignments.filter(
            Q(booking__booking_id__icontains=filter_assignment)
        )



    paginator = Paginator(all_assignments, page_size)

    try:
        paginated_assignments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_assignments = paginator.page(1)
    except EmptyPage:
        paginated_assignments = paginator.page(paginator.num_pages)

    all_assignment_serializer = AllBookedGuardsSerializer(paginated_assignments, many=True)


    data['guard_assignments'] = all_assignment_serializer.data
    data['pagination'] = {
        'page_number': paginated_assignments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_assignments.next_page_number() if paginated_assignments.has_next() else None,
        'previous': paginated_assignments.previous_page_number() if paginated_assignments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

