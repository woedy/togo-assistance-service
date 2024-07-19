
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from human_resources.api.serializers import AllStaffPayPeriodsSerializer, StaffPayPeriodDetailsSerializer
from human_resources.models import StaffPayPeriod

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_staff_pay_period(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        start_date = request.data.get('start_date', "")
        end_date = request.data.get('end_date', "")


        if not start_date:
            errors['start_date'] = ['Start date is required.']
        if not end_date:
            errors['end_date'] = ['End date is required.']


        try:
            payment_period = StaffPayPeriod.objects.get(
                start_date=start_date,
                end_date=end_date
            )
            errors['id'] = ['Staff Pay period already exist.']
        except:
            pass



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_payment_period = StaffPayPeriod.objects.create(
            start_date=start_date,
            end_date=end_date

        )

        data['id'] = new_payment_period.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_staff_pay_period_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_pay_periods = StaffPayPeriod.objects.all().filter(is_archived=False)


    if search_query:
        all_pay_periods = all_pay_periods.filter(
            Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )


    paginator = Paginator(all_pay_periods, page_size)

    try:
        paginated_pay_periods = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_pay_periods = paginator.page(1)
    except EmptyPage:
        paginated_pay_periods = paginator.page(paginator.num_pages)

    all_pay_periods_serializer = AllStaffPayPeriodsSerializer(paginated_pay_periods, many=True)


    data['pay_period'] = all_pay_periods_serializer.data
    data['pagination'] = {
        'page_number': paginated_pay_periods.number,
        'total_pages': paginator.num_pages,
        'next': paginated_pay_periods.next_page_number() if paginated_pay_periods.has_next() else None,
        'previous': paginated_pay_periods.previous_page_number() if paginated_pay_periods.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_pay_staff_period_details_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.query_params.get('id', None)

    if not id:
        errors['id'] = ["ID required"]

    try:
        pay_period = StaffPayPeriod.objects.get(id=id)
    except:
        errors['id'] = ['Staff Pay period does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    pay_period_serializer = StaffPayPeriodDetailsSerializer(pay_period, many=False)
    if pay_period_serializer:
        pay_period = pay_period_serializer.data


    payload['message'] = "Successful"
    payload['data'] = pay_period

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_staff_pay_period(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")
        start_date = request.data.get('start_date', "")
        end_date = request.data.get('end_date', "")
        is_closed = request.data.get('is_closed', "")


        if not id:
            errors['id'] = ['ID is required.']
        if not start_date:
            errors['start_date'] = ['Start date is required.']
        if not end_date:
            errors['end_date'] = ['End date is required.']

        if not is_closed:
            errors['is_closed'] = ['Closing Boolean is required.']

        try:
            pay_period = StaffPayPeriod.objects.get(id=id)
        except:
            errors['id'] = ['Staff Pay Period does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        pay_period.start_date=start_date
        pay_period.end_date=end_date
        pay_period.is_closed=is_closed
        pay_period.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_staff_pay_period(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['ID is required.']

        try:
            pay_period = StaffPayPeriod.objects.get(id=id)
        except:
            errors['id'] = ['Staff Pay Period does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        pay_period.is_archived = True
        pay_period.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_staff_pay_period(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['ID is required.']

        try:
            pay_period = StaffPayPeriod.objects.get(id=id)
        except:
            errors['id'] = ['Staff Pay Period does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        pay_period.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_staff_pay_period(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['ID is required.']

        try:
            pay_period = StaffPayPeriod.objects.get(id=id)
        except:
            errors['id'] = ['Pay Period does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        pay_period.is_archived = False
        pay_period.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)













@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_staff_pay_period_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_pay_periods = StaffPayPeriod.objects.all().filter(is_archived=True)


    if search_query:
        all_pay_periods = all_pay_periods.filter(
            Q(start_date__icontains=search_query) |
            Q(end_date__icontains=search_query)
        )


    paginator = Paginator(all_pay_periods, page_size)

    try:
        paginated_pay_periods = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_pay_periods = paginator.page(1)
    except EmptyPage:
        paginated_pay_periods = paginator.page(paginator.num_pages)

    all_pay_periods_serializer = AllStaffPayPeriodsSerializer(paginated_pay_periods, many=True)


    data['pay_period'] = all_pay_periods_serializer.data
    data['pagination'] = {
        'page_number': paginated_pay_periods.number,
        'total_pages': paginator.num_pages,
        'next': paginated_pay_periods.next_page_number() if paginated_pay_periods.has_next() else None,
        'previous': paginated_pay_periods.previous_page_number() if paginated_pay_periods.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

