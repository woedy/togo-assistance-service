
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from billing.api.serializers import AllPayPeriodsSerializer, PayPeriodDetailsSerializer, AllPayrollEntrysSerializer, \
    PayrollEntryDetailsSerializer

from security_team.models import PayPeriod, SecurityGuard, PayrollEntry

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        pay_period_id = request.data.get('pay_period_id', "")
        basic_salary = request.data.get('basic_salary', 0)
        overtime_hours = request.data.get('overtime_hours', 0)
        overtime_rate = request.data.get('overtime_rate', 0)
        deductions = request.data.get('deductions', 0)




        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not pay_period_id:
            errors['pay_period_id'] = ['Pay Period ID is required.']

        if not basic_salary:
            errors['basic_salary'] = ['Basic Salary is required.']

        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']


        try:
            pay_period = PayPeriod.objects.get(id=pay_period_id)
        except:
            errors['pay_period_id'] = ['Pay Period does not exist.']

        try:
            payroll = PayrollEntry.objects.get(guard=guard, pay_period=pay_period)
            errors['payroll_id'] = ['Payroll already exist.']
        except:
            pass

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_pay_period = PayrollEntry.objects.create(
            guard=guard,
            pay_period=pay_period,
            basic_salary=basic_salary,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate,
            deductions=deductions,

        )
        data['payroll_id'] = new_pay_period.payroll_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_payroll_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payroll_entrys = PayrollEntry.objects.all().filter(is_archived=False)


    if search_query:
        all_payroll_entrys = all_payroll_entrys.filter(
            Q(guard__guard_id__icontains=search_query) |
            Q(pay_period__start_date__icontains=search_query)
        )


    paginator = Paginator(all_payroll_entrys, page_size)

    try:
        paginated_payroll_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_payroll_entrys = paginator.page(1)
    except EmptyPage:
        paginated_payroll_entrys = paginator.page(paginator.num_pages)

    all_payroll_entrys_serializer = AllPayrollEntrysSerializer(paginated_payroll_entrys, many=True)


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
def get_payroll_entry_details_view(request):
    payload = {}
    data = {}
    errors = {}

    payroll_id = request.query_params.get('payroll_id', None)

    if not payroll_id:
        errors['payroll_id'] = ["Payroll ID required"]

    try:
        payroll_entry = PayrollEntry.objects.get(payroll_id=payroll_id)
    except:
        errors['payroll_id'] = ['Payroll Entry does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    payroll_entry_serializer = PayrollEntryDetailsSerializer(payroll_entry, many=False)
    if payroll_entry_serializer:
        payroll_entry = payroll_entry_serializer.data


    payload['message'] = "Successful"
    payload['data'] = payroll_entry

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payroll_id = request.data.get('payroll_id', "")

        guard_id = request.data.get('guard_id', "")
        pay_period_id = request.data.get('pay_period_id', "")
        basic_salary = request.data.get('basic_salary', "")
        overtime_hours = request.data.get('overtime_hours', "")
        overtime_rate = request.data.get('overtime_rate', "")
        deductions = request.data.get('deductions', "")




        if not payroll_id:
            errors['payroll_id'] = ['Payroll ID is required.']


        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not pay_period_id:
            errors['pay_period_id'] = ['Pay Period ID is required.']

        if not basic_salary:
            errors['basic_salary'] = ['Basic Salary is required.']

        try:
            payroll_entry = PayrollEntry.objects.get(payroll_id=payroll_id)
        except:
            errors['payroll_id'] = ['Payroll entry does not exist.']

        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']

        try:
            pay_period = PayPeriod.objects.get(id=pay_period_id)
        except:
            errors['pay_period_id'] = ['Pay Period does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_pay_period = PayrollEntry.objects.create(
            guard=guard,
            pay_period=pay_period,
            basic_salary=basic_salary,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate,
            deductions=deductions,

        )


        payroll_entry.guard = guard
        payroll_entry.pay_period = pay_period
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
def archive_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payroll_id = request.data.get('payroll_id', "")

        if not payroll_id:
            errors['payroll_id'] = ['ID is required.']

        try:
            payroll_entry = PayrollEntry.objects.get(payroll_id=payroll_id)
        except:
            errors['payroll_id'] = ['Payroll Entry does not exist.']


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
def delete_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payroll_id = request.data.get('payroll_id', "")

        if not payroll_id:
            errors['payroll_id'] = ['ID is required.']

        try:
            payroll_entry = PayrollEntry.objects.get(payroll_id=payroll_id)
        except:
            errors['payroll_id'] = ['Payroll Entry does not exist.']

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
def unarchive_payroll_entry(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        payroll_id = request.data.get('payroll_id', "")

        if not payroll_id:
            errors['payroll_id'] = ['ID is required.']

        try:
            payroll_entry = PayrollEntry.objects.get(payroll_id=payroll_id)
        except:
            errors['payroll_id'] = ['Payroll Entry does not exist.']

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
def get_all_archived_payroll_entry_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_payroll_entrys = PayrollEntry.objects.all().filter(is_archived=True)


    if search_query:
        all_payroll_entrys = all_payroll_entrys.filter(
            Q(guard__guard_id__icontains=search_query) |
            Q(pay_period__start_date__icontains=search_query)
        )


    paginator = Paginator(all_payroll_entrys, page_size)

    try:
        paginated_payroll_entrys = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_payroll_entrys = paginator.page(1)
    except EmptyPage:
        paginated_payroll_entrys = paginator.page(paginator.num_pages)

    all_payroll_entrys_serializer = AllPayrollEntrysSerializer(paginated_payroll_entrys, many=True)


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

