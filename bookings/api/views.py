from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import Booking, BookDate
from clients.models import Client


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_generic_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")


        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client ID is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        new_client_request = Booking.objects.create(
            client=client
        )
        request_dates = BookDate.objects.create(
            booking=new_client_request
        )



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_basic_info_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        guard_type = request.data.get('guard_type', "")
        equipment_requirements = request.data.get('equipment_requirements', "")
        special_instruction = request.data.get('special_instruction', "")


        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not guard_type:
            errors['guard_type'] = ['Guard type is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_client_request = Booking.objects.create(
            client=client,
            guard_type=guard_type,
            equipment_requirements=equipment_requirements,
            special_instruction=special_instruction,
        )

        data['booking_id'] = new_client_request.booking_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_basic_zones_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        zone_name = request.data.get('zone_name', "")
        description = request.data.get('description', "")
        coordinates = request.data.get('coordinates', "")


        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not zone_name:
            errors['zone_name'] = ['Zone name is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_client_zone = ClientZone.objects.create(
            client=client,
            zone_name=zone_name,
            description=description,
        )
        for coordinate in coordinates:
            zone_coordinate = ClientZone.objects.create(
                client_zone=new_client_zone,
                lat=coordinate['lat'],
                lng=coordinate['lng'],
            )


        data['zone_id'] = new_client_zone.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_basic_zone_sites_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        zone_id = request.data.get('zone_id', "")

        site_name = request.data.get('site_name', "")
        description = request.data.get('description', "")
        lat = request.data.get('lat', "")
        lng = request.data.get('lng', "")
        location_name = request.data.get('location_name', "")
        no_of_guards = request.data.get('no_of_guards', "")
        guards_gender = request.data.get('guards_gender', "")
        site_type = request.data.get('site_type', "")


        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not zone_id:
            errors['zone_id'] = ['Zone ID is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']


        try:
            zone = ClientZone.objects.get(client=client)
        except:
            errors['zone'] = ['Zone does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_zone_site = ClientPostSite.objects.create(
            client=client,
            zone=zone,
            description=description,
            lat=lat,
            lng=lng,
            location_name=location_name,
            no_of_guards=no_of_guards,
            guards_gender=guards_gender,
            site_type=site_type,
        )

        data['site_id'] = new_zone_site.id



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_date_times_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        client_id = request.data.get('client_id', "")
        booking_id = request.data.get('booking_id', "")

        book_dates = request.data.get('book_dates', "")


        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not book_dates:
            errors['book_dates'] = ['Enter at least one book date and time.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        for date in book_dates:
            new_book_date = BookDate.objects.create(
                booking=booking,
                booking_date=booking_date,
                from_time=from_time,
                to_time=to_time,
            )




        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

