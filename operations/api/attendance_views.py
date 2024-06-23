from datetime import timezone

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import Booking, Deployment, DeploymentAttendance
from operations.api.serializers import AllDeploymentsSerializer, DeploymentDetailsSerializer, \
    AllDeploymentAttendancesSerializer, DeploymentAttendanceDetailsSerializer
from operations.models import Operation
from security_team.models import SecurityGuard


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def clock_in_guard(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        deployment_id = request.data.get('deployment_id', "")
        guard_id = request.data.get('guard_id', "")
        note = request.data.get('note', "")


        if not deployment_id:
            errors['deployment_id'] = ['Deployment ID is required.']

        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']



        try:
            deployment = Deployment.objects.get(deployment_id=deployment_id)
        except:
            errors['deployment_id'] = ['Deployment does not exist.']


        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_clock_in = DeploymentAttendance.objects.create(
            deployment=deployment,
            guard=guard,
            note=note,
            clock_in=timezone.now(),
        )


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def clock_out_guard(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        deployment_id = request.data.get('deployment_id', "")
        guard_id = request.data.get('guard_id', "")
        note = request.data.get('note', "")


        if not deployment_id:
            errors['deployment_id'] = ['Deployment ID is required.']

        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']



        try:
            deployment = Deployment.objects.get(deployment_id=deployment_id)
        except:
            errors['deployment_id'] = ['Deployment does not exist.']


        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_clock_out = DeploymentAttendance.objects.create(
            deployment=deployment,
            guard=guard,
            note=note,
            clock_out=timezone.now(),
        )


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_attendances(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    filter_attendance = request.query_params.get('filter_attendance', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_attendances = DeploymentAttendance.objects.filter(is_archived=False)


    if search_query:
        all_attendances = all_attendances.filter(
            Q(deployment_deployment_id__icontains=search_query) |
            Q(guard_guard_id__icontains=search_query)
        )



    if filter_attendance:
        all_attendances = all_attendances.filter(
            Q(deployment_deployment_id__icontains=filter_attendance) |
            Q(guard_guard_id__icontains=filter_attendance)
        )



    paginator = Paginator(all_attendances, page_size)

    try:
        paginated_attendances = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_attendances = paginator.page(1)
    except EmptyPage:
        paginated_attendances = paginator.page(paginator.num_pages)

    all_attendances_serializer = AllDeploymentAttendancesSerializer(paginated_attendances, many=True)


    data['attendances'] = all_attendances_serializer.data
    data['pagination'] = {
        'page_number': paginated_attendances.number,
        'total_pages': paginator.num_pages,
        'next': paginated_attendances.next_page_number() if paginated_attendances.has_next() else None,
        'previous': paginated_attendances.previous_page_number() if paginated_attendances.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_attendance_details_view(request):
    payload = {}
    data = {}
    errors = {}

    attendance_id = request.query_params.get('attendance_id', None)

    if not attendance_id:
        errors['attendance_id'] = ["Attendance id required"]

    try:
        attendance = DeploymentAttendance.objects.get(id=attendance_id)
    except:
        errors['attendance_id'] = ['Attendance does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    attendance_serializer = DeploymentAttendanceDetailsSerializer(attendance, many=False)
    if attendance_serializer:
        attendance = attendance_serializer.data


    payload['message'] = "Successful"
    payload['data'] = attendance

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_attendance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        attendance_id = request.data.get('attendance_id', "")

        if not attendance_id:
            errors['attendance_id'] = ['Attendance ID is required.']

        try:
            attendance = DeploymentAttendance.objects.get(id=attendance_id)
        except:
            errors['attendance_id'] = ['Attendance does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        attendance.is_archived = True
        attendance.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_attendance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        attendance_id = request.data.get('attendance_id', "")

        if not attendance_id:
            errors['attendance_id'] = ['Attendance ID is required.']

        try:
            attendance = DeploymentAttendance.objects.get(id=attendance_id)
        except:
            errors['attendance_id'] = ['Attendance does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        attendance.is_archived = False
        attendance.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_attendance(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        attendance_id = request.data.get('attendance_id', "")

        if not attendance_id:
            errors['attendance_id'] = ['Attendance ID is required.']

        try:
            attendance = DeploymentAttendance.objects.get(id=attendance_id)
        except:
            errors['attendance_id'] = ['Attendance does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        attendance.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_attendances_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    filter_attendance = request.query_params.get('filter_attendance', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_attendances = DeploymentAttendance.objects.filter(is_archived=True)


    if search_query:
        all_attendances = all_attendances.filter(
            Q(deployment_deployment_id__icontains=search_query) |
            Q(guard_guard_id__icontains=search_query)
        )



    if filter_attendance:
        all_attendances = all_attendances.filter(
            Q(deployment_deployment_id__icontains=filter_attendance) |
            Q(guard_guard_id__icontains=filter_attendance)
        )



    paginator = Paginator(all_attendances, page_size)

    try:
        paginated_attendances = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_attendances = paginator.page(1)
    except EmptyPage:
        paginated_attendances = paginator.page(paginator.num_pages)

    all_attendances_serializer = AllDeploymentAttendancesSerializer(paginated_attendances, many=True)


    data['attendances'] = all_attendances_serializer.data
    data['pagination'] = {
        'page_number': paginated_attendances.number,
        'total_pages': paginator.num_pages,
        'next': paginated_attendances.next_page_number() if paginated_attendances.has_next() else None,
        'previous': paginated_attendances.previous_page_number() if paginated_attendances.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


