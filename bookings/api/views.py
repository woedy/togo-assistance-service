from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.api.serializers import AllBookingsSerializer, BookingDetailsSerializer
from bookings.models import Booking, BookDate
from clients.models import Client
from post_sites.models import ClientZone, ClientZoneCoordinate, ClientPostSite


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
def add_client_request_basic_zone_view(request):
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
            zone_coordinate = ClientZoneCoordinate.objects.create(
                client_zone=new_client_zone,
                lat=coordinate[0],
                lng=coordinate[1],
            )


        data['zone_id'] = new_client_zone.zone_id


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
        zone_id = request.data.get('zone_id', "")

        sites = request.data.get('sites', "")


        if not zone_id:
            errors['zone_id'] = ['Zone ID is required.']

        if not sites:
            errors['sites'] = ['At least one site is required.']


        try:
            zone = ClientZone.objects.get(zone_id=zone_id)
        except:
            errors['zone'] = ['Zone does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        print(sites)

        for site in sites:
            print("site[description######################")
            print(site)
            new_zone_site = ClientPostSite.objects.create(
                client_zone=zone,
                description=site["description"],
                lat=site["lat"],
                lng=site["lng"],
                location_name=site["location_name"],
                no_of_guards=site["no_of_guards"],
                guards_gender=site["guards_gender"],
                site_type=site["site_type"],
            )

        data['site_id'] = new_zone_site.site_id



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
        booking_id = request.data.get('booking_id', "")

        book_dates = request.data.get('book_dates', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not book_dates:
            errors['book_dates'] = ['Enter at least one book date and time.']

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
                booking_date=date["booking_date"],
                from_time=date["from_time"],
                to_time=date["to_time"],
            )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_client_requests(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_bookings = Booking.objects.all().filter(is_archived=False)


    if search_query:
        all_bookings = all_bookings.filter(
            Q(booking_id__icontains=search_query)
        )


    paginator = Paginator(all_bookings, page_size)

    try:
        paginated_bookings = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_bookings = paginator.page(1)
    except EmptyPage:
        paginated_bookings = paginator.page(paginator.num_pages)

    all_bookings_serializer = AllBookingsSerializer(paginated_bookings, many=True)


    data['bookings'] = all_bookings_serializer.data
    data['pagination'] = {
        'page_number': paginated_bookings.number,
        'total_pages': paginator.num_pages,
        'next': paginated_bookings.next_page_number() if paginated_bookings.has_next() else None,
        'previous': paginated_bookings.previous_page_number() if paginated_bookings.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_client_request_details(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.query_params.get('booking_id', None)

    if not booking_id:
        errors['booking_id'] = ["Booking ID required"]

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    booking_serializer = BookingDetailsSerializer(booking, many=False)
    if booking_serializer:
        booking = booking_serializer.data


    payload['message'] = "Successful"
    payload['data'] = booking

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_client_request(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        client_id = request.data.get('client_id', "")
        guard_type = request.data.get('guard_type', "")
        equipment_requirements = request.data.get('equipment_requirements', "")
        special_instruction = request.data.get('special_instruction', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']


        if not guard_type:
            errors['guard_type'] = ['Guard type is required.']


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


        booking.guard_type = guard_type
        booking.equipment_requirements = equipment_requirements
        booking.special_instruction = special_instruction
        booking.save()

        data['booking_id'] = booking.booking_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_client_request_zone(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        zone_id = request.data.get('zone_id', "")
        client_id = request.data.get('client_id', "")
        zone_name = request.data.get('zone_name', "")
        description = request.data.get('description', "")
        coordinates = request.data.get('coordinates', "")

        if not zone_id:
            errors['zone_id'] = ['Zone ID is required.']

        if not client_id:
            errors['client_id'] = ['Client ID is required.']

        if not zone_name:
            errors['zone_name'] = ['Zone name is required.']

        try:
            client = Client.objects.get(client_id=client_id)
        except:
            errors['client_id'] = ['Client does not exist.']

        try:
            zone = ClientZone.objects.get(zone_id=zone_id)
        except:
            errors['zone_id'] = ['Zone does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        zone.zone_name = zone_name
        zone.description = description
        zone.save()

        _coordinates = ClientZoneCoordinate.objects.filter(client_zone=zone)
        for coord in _coordinates:
            coord.delete()

        for coordinate in coordinates:
            zone_coordinate = ClientZoneCoordinate.objects.create(
                client_zone=zone,
                lat=coordinate[0],
                lng=coordinate[1],
            )




        data['zone_id'] = zone.zone_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_client_request_zone_site(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_id = request.data.get('site_id', "")
        site_name = request.data.get('site_name', "")
        description = request.data.get('description', "")
        lat = request.data.get('lat', "")
        lng = request.data.get('lng', "")
        location_name = request.data.get('location_name', "")
        no_of_guards = request.data.get('no_of_guards', "")
        guards_gender = request.data.get('guards_gender', "")
        site_type = request.data.get('site_type', "")

        if not site_id:
            errors['site_id'] = ['Site ID is required.']

        if not site_name:
            errors['site_name'] = ['Site name is required.']


        try:
            site = ClientPostSite.objects.get(site_id=site_id)
        except:
            errors['site_id'] = ['Site does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        site.site_name = site_name
        site.description = description
        site.lat = lat
        site.lng = lng
        site.location_name = location_name
        site.no_of_guards = no_of_guards
        site.guards_gender = guards_gender
        site.site_type = site_type
        site.save()


        data['site_id'] = site.site_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_client_request_datetime(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")
        booking_date = request.data.get('booking_date', "")
        from_time = request.data.get('from_time', "")
        to_time = request.data.get('to_time', "")

        if not id:
            errors['id'] = ['Book date ID is required.']

        if not booking_date:
            errors['booking_date'] = ['Book date is required.']


        if not from_time:
            errors['from_time'] = ['From time is required.']

        if not to_time:
            errors['to_time'] = ['To time is required.']


        try:
            _datetime = BookDate.objects.get(id=id)
        except:
            errors['id'] = ['Booking date does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        _datetime.booking_date = booking_date
        _datetime.from_time = from_time
        _datetime.to_time = to_time
        _datetime.save()


        data['id'] = _datetime.id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_client_request(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking.is_archived = True
        booking.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_client_request(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking.is_archived = False
        booking.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_client_request(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

