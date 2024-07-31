from datetime import datetime, date, timedelta

from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from security_team.api.serializers import GuardAvailabilitySerializer
from security_team.models import SecurityGuard, GuardAvailability, TimeSlot

User = get_user_model()


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def set_guard_availability(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        availability = request.data.get('availability', [])
        print("###########################################################")
        print("###########################################################")
        print(guard_id)
        print(availability)
        

        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']



        if not availability:
            errors['availability'] = ['Availability is required.']



        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)


            # Fetch the existing slots for the guard
            existing_slots = GuardAvailability.objects.filter(guard=guard)
            existing_slot_dates = existing_slots.values_list('slot_date', flat=True)

            for slot_data in availability:
                slot_date = slot_data.get('date')
                new_time_slots = slot_data.get('time_slots')
                # Convert the times to datetime objects
                time_objects = [datetime.strptime(t, "%H:%M:%S" if len(t) > 5 else "%H:%M").time() for t in slot_data['time_slots']]

                # Check if a slot with the same date already exists
                existing_slot = existing_slots.filter(slot_date=slot_date).first()
                if existing_slot:
                    # Slot already exists, update it
                    existing_time_slots = TimeSlot.objects.filter(guard_slot=existing_slot)
                    # Iterate through the new time slots
                    for time in new_time_slots:
                        existing_time_slot = existing_time_slots.filter(time=time).first()
                        if existing_time_slot:
                            if existing_time_slot.occupied:
                                # Time slot is occupied, continue to the next slot
                                continue
                        else:
                            # Create a new time slot if it doesn't exist
                            TimeSlot.objects.create(
                                guard_slot=existing_slot,
                                time=time,
                                occupied=False
                            )
                    # Delete time slots that are not in the new list
                    existing_time_slots.filter(~Q(time__in=new_time_slots)).delete()
                else:
                    # Slot doesn't exist, create a new slot
                    new_slot = GuardAvailability.objects.create(guard=guard, slot_date=slot_date)
                    for time in new_time_slots:
                        TimeSlot.objects.create(
                            guard_slot=new_slot,
                            time=time,
                            occupied=False
                        )
            # Delete slots that are not in the new list
            existing_slots.filter(~Q(slot_date__in=[s['date'] for s in availability])).delete()

        except:
            errors['guard_id'] = ['Guard does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payload['message'] = "Slot added or updated successfully"
        payload['data'] = data

        return Response(payload)










@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def list_guard_availability(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")

        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except SecurityGuard.DoesNotExist:
            errors['guard_id'] = ['Guard does not exist']
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        availability_interval = "1 hour"

        # Calculate the datetime threshold based on the specified interval
        current_datetime = datetime.now()
        interval_mapping = {
            "1 hour": timedelta(hours=1),
            "6 hours": timedelta(hours=6),
            "12 hours": timedelta(hours=12),
            "8 hours": timedelta(hours=8),
            "24 hours": timedelta(hours=24),
            "48 hours": timedelta(hours=48)
        }
        threshold_datetime = current_datetime + interval_mapping.get(availability_interval, timedelta(hours=1))

        # Filter availability slots based on the threshold_datetime
        all_guard_slots = GuardAvailability.objects.filter(
            guard=guard,
            slot_date__gte=threshold_datetime.date(),
        )

        for _slot in all_guard_slots:
            if str(current_datetime.date()) == str(_slot.slot_date):
                # check slots with times before the threshold time
                print(_slot.slot_date)
                # print(_slot.slot_times)

        all_guard_slots_serializer = GuardAvailabilitySerializer(all_guard_slots, many=True)
        _all_guard_slots = all_guard_slots_serializer.data
        data['all_guard_availability'] = _all_guard_slots

        payload['message'] = "Successful"
        payload['data'] = data
        return Response(payload)

    return Response({'message': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

