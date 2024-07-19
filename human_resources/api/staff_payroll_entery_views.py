
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from human_resources.api.serializers import AllStaffPayrollEntrysSerializer, StaffPayrollEntryDetailsSerializer
from human_resources.models import StaffPayrollEntry, StaffPayPeriod

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_staff_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        pay_period_id = request.data.get('pay_period_id', "")
        basic_salary = request.data.get('basic_salary', 0)
        overtime_hours = request.data.get('overtime_hours', 0)
        overtime_rate = request.data.get('overtime_rate', 0)
        deductions = request.data.get('deductions', 0)




        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not pay_period_id:
            errors['pay_period_id'] = ['Pay Period ID is required.']

        if not basic_salary:
            errors['basic_salary'] = ['Basic Salary is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        try:
            pay_period = StaffPayPeriod.objects.get(id=pay_period_id)
        except:
            errors['staff_pay_period_id'] = ['Staff Pay Period does not exist.']

        try:
            payroll = StaffPayrollEntry.objects.get(user=user, pay_period=pay_period)
            errors['staff_payroll_id'] = ['Staff Payroll already exist.']
        except:
            pass

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_pay_period = StaffPayrollEntry.objects.create(
            staff=user,
            staff_pay_period=pay_period,
            basic_salary=basic_salary,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate,
            deductions=deductions,

        )
        data['staff_payroll_id'] = new_pay_period.staff_payroll_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_staff_payroll_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payroll_entrys = StaffPayrollEntry.objects.all().filter(is_archived=False)


    if search_query:
        all_payroll_entrys = all_payroll_entrys.filter(
            Q(user__user_id__icontains=search_query) |
            Q(staff_pay_period__start_date__icontains=search_query)
        )


    paginator = Paginator(all_payroll_entrys, page_size)

    try:
        paginated_payroll_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_payroll_entrys = paginator.page(1)
    except EmptyPage:
        paginated_payroll_entrys = paginator.page(paginator.num_pages)

    all_payroll_entrys_serializer = AllStaffPayrollEntrysSerializer(paginated_payroll_entrys, many=True)


    data['payroll_entries'] = all_payroll_entrys_serializer.data
    data['pagination'] = {
        'page_number': paginated_payroll_entrys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_payroll_entrys.next_page_number() if paginated_payroll_entrys.has_next() else None,
        'previous': paginated_payroll_entrys.previous_page_number() if paginated_payroll_entrys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_staff_payroll_entry_details_view(request):
    payload = {}
    data = {}
    errors = {}

    staff_payroll_id = request.query_params.get('staff_payroll_id', None)

    if not staff_payroll_id:
        errors['staff_payroll_id'] = ["Staff Payroll ID required"]

    try:
        payroll_entry = StaffPayrollEntry.objects.get(staff_payroll_id=staff_payroll_id)
    except:
        errors['staff_payroll_id'] = ['Staff Payroll Entry does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    payroll_entry_serializer = StaffPayrollEntryDetailsSerializer(payroll_entry, many=False)
    if payroll_entry_serializer:
        payroll_entry = payroll_entry_serializer.data


    payload['message'] = "Successful"
    payload['data'] = payroll_entry

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_staff_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_payroll_id = request.data.get('staff_payroll_id', "")

        user_id = request.data.get('user_id', "")
        pay_period_id = request.data.get('pay_period_id', "")
        basic_salary = request.data.get('basic_salary', "")
        overtime_hours = request.data.get('overtime_hours', "")
        overtime_rate = request.data.get('overtime_rate', "")
        deductions = request.data.get('deductions', "")




        if not staff_payroll_id:
            errors['staff_payroll_id'] = ['Staff Payroll ID is required.']


        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not pay_period_id:
            errors['pay_period_id'] = ['Pay Period ID is required.']

        if not basic_salary:
            errors['basic_salary'] = ['Basic Salary is required.']

        try:
            payroll_entry = StaffPayrollEntry.objects.get(staff_payroll_id=staff_payroll_id)
        except:
            errors['staff_payroll_id'] = ['staff Payroll entry does not exist.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        try:
            pay_period = StaffPayPeriod.objects.get(id=pay_period_id)
        except:
            errors['staff_pay_period_id'] = ['Staff Pay Period does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)



        payroll_entry.staff = user
        payroll_entry.staff_pay_period = pay_period
        payroll_entry.basic_salary = basic_salary
        payroll_entry.overtime_hours = overtime_hours
        payroll_entry.overtime_rate = overtime_rate
        payroll_entry.deductions = deductions

        payroll_entry.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_staff_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_payroll_id = request.data.get('staff_payroll_id', "")

        if not staff_payroll_id:
            errors['staff_payroll_id'] = ['ID is required.']

        try:
            payroll_entry = StaffPayrollEntry.objects.get(staff_payroll_id=staff_payroll_id)
        except:
            errors['staff_payroll_id'] = ['Staff Payroll Entry does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payroll_entry.is_archived = True
        payroll_entry.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_staff_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_payroll_id = request.data.get('staff_payroll_id', "")

        if not staff_payroll_id:
            errors['staff_payroll_id'] = ['ID is required.']

        try:
            payroll_entry = StaffPayrollEntry.objects.get(staff_payroll_id=staff_payroll_id)
        except:
            errors['staff_payroll_id'] = ['Staff Payroll Entry does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payroll_entry.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_staff_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        staff_payroll_id = request.data.get('staff_payroll_id', "")

        if not staff_payroll_id:
            errors['staff_payroll_id'] = ['ID is required.']

        try:
            payroll_entry = StaffPayrollEntry.objects.get(staff_payroll_id=staff_payroll_id)
        except:
            errors['staff_payroll_id'] = ['Staff Payroll Entry does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        payroll_entry.is_archived = False
        payroll_entry.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_staff_payroll_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payroll_entrys = StaffPayrollEntry.objects.all().filter(is_archived=True)


    if search_query:
        all_payroll_entrys = all_payroll_entrys.filter(
            Q(user__user_id__icontains=search_query) |
            Q(pay_period__start_date__icontains=search_query)
        )


    paginator = Paginator(all_payroll_entrys, page_size)

    try:
        paginated_payroll_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_payroll_entrys = paginator.page(1)
    except EmptyPage:
        paginated_payroll_entrys = paginator.page(paginator.num_pages)

    all_payroll_entrys_serializer = AllStaffPayrollEntrysSerializer(paginated_payroll_entrys, many=True)


    data['payroll_entries'] = all_payroll_entrys_serializer.data
    data['pagination'] = {
        'page_number': paginated_payroll_entrys.number,
        'total_pages': paginator.num_pages,
        'next': paginated_payroll_entrys.next_page_number() if paginated_payroll_entrys.has_next() else None,
        'previous': paginated_payroll_entrys.previous_page_number() if paginated_payroll_entrys.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

