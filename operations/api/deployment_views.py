from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import Booking, Deployment
from operations.api.serializers import AllDeploymentsSerializer, DeploymentDetailsSerializer, OperationsDetailsSerializer
from operations.models import Operation
from post_sites.models import ClientPostSite
from security_team.models import SecurityGuard


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def assign_supervisor(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        supervisor_id = request.data.get('supervisor_id', "")
        site_id = request.data.get('site_id', "")
        guards = request.data.get('guards', [])


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not supervisor_id:
            errors['supervisor_id'] = ['Supervisor ID is required.']

        if not site_id:
            errors['site_id'] = ['Site ID is required.']

        if not guards:
            errors['guards'] = ['Required is required.']



        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']


        try:
            supervisor = Operation.objects.get(operations_id=supervisor_id)
        except:
            errors['supervisor_id'] = ['Supervisor does not exist.']

        try:
            site = ClientPostSite.objects.get(site_id=site_id)
        except:
            errors['site_id'] = ['Site does not exist.']


        try:
            deployment = Deployment.objects.get(booking=booking, supervisor=supervisor)
            errors['booking_id'] = ['Supervisor already assigned.']
        except:
            pass

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_deployment = Deployment.objects.create(
            booking=booking,
            supervisor=supervisor,
            site=site
        )

        for guard in guards:
            print("##########################")
            print(guard)

            _guard = SecurityGuard.objects.get(guard_id=guard)
            new_deployment.guards.add(_guard)
            new_deployment.save()


        data['deployment_id'] = new_deployment.deployment_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_deployments(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_deployments = Deployment.objects.filter(is_archived=False)


    if search_query:
        all_deployments = all_deployments.filter(
            Q(booking__booking_id__icontains=search_query) |
            Q(supervisor__operations_id__icontains=search_query)

        )

    if filer_supervisor:
        all_deployments = all_deployments.filter(
            Q(supervisor__operations_id__icontains=filer_supervisor)

        )



    paginator = Paginator(all_deployments, page_size)

    try:
        paginated_deployments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_deployments = paginator.page(1)
    except EmptyPage:
        paginated_deployments = paginator.page(paginator.num_pages)

    all_deployments_serializer = AllDeploymentsSerializer(paginated_deployments, many=True)


    data['deployments'] = all_deployments_serializer.data
    data['pagination'] = {
        'page_number': paginated_deployments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_deployments.next_page_number() if paginated_deployments.has_next() else None,
        'previous': paginated_deployments.previous_page_number() if paginated_deployments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_supervisors(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_operations = Operation.objects.all().filter(user__is_archived=False).filter(role='Supervisor')


    if search_query:
        all_operations = all_operations.filter(
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__department__icontains=search_query) |
            Q(user__gender__icontains=search_query) |
            Q(user__dob__icontains=search_query) |
            Q(user__marital_status__icontains=search_query) |
            Q(user__phone__icontains=search_query) |
            Q(user__country__icontains=search_query) |
            Q(user__language__icontains=search_query) |
            Q(user__location_name__icontains=search_query)
        )


    paginator = Paginator(all_operations, page_size)

    try:
        paginated_operations = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_operations = paginator.page(1)
    except EmptyPage:
        paginated_operations = paginator.page(paginator.num_pages)

    all_operations_serializer = OperationsDetailsSerializer(paginated_operations, many=True)


    data['supervisors'] = all_operations_serializer.data
    data['pagination'] = {
        'page_number': paginated_operations.number,
        'total_pages': paginator.num_pages,
        'next': paginated_operations.next_page_number() if paginated_operations.has_next() else None,
        'previous': paginated_operations.previous_page_number() if paginated_operations.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_deployment_details_view(request):
    payload = {}
    data = {}
    errors = {}

    deployment_id = request.query_params.get('deployment_id', None)

    if not deployment_id:
        errors['deployment_id'] = ["Deployment id required"]

    try:
        deployment = Deployment.objects.get(deployment_id=deployment_id)
    except Deployment.DoesNotExist:
        errors['deployment_id'] = ['Deployment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    deployment_serializer = DeploymentDetailsSerializer(deployment, many=False)
    if deployment_serializer:
        deployment = deployment_serializer.data


    payload['message'] = "Successful"
    payload['data'] = deployment

    return Response(payload, status=status.HTTP_200_OK)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_deployment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        deployment_id = request.data.get('deployment_id', "")

        if not deployment_id:
            errors['deployment_id'] = ['Deployment ID is required.']

        try:
            deployment = Deployment.objects.get(deployment_id=deployment_id)
        except:
            errors['deployment_id'] = ['Deployment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        deployment.is_archived = True
        deployment.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_deployment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        deployment_id = request.data.get('deployment_id', "")

        if not deployment_id:
            errors['deployment_id'] = ['Deployment ID is required.']

        try:
            deployment = Deployment.objects.get(deployment_id=deployment_id)
        except:
            errors['deployment_id'] = ['Deployment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        deployment.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_deployment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        deployment_id = request.data.get('deployment_id', "")

        if not deployment_id:
            errors['deployment_id'] = ['Deployment ID is required.']

        try:
            deployment = Deployment.objects.get(deployment_id=deployment_id)
        except:
            errors['deployment_id'] = ['Deployment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        deployment.is_archived = False
        deployment.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_deployments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_deployments = Deployment.objects.filter(is_archived=True)


    if search_query:
        all_deployments = all_deployments.filter(
            Q(booking_booking_id__icontains=search_query) |
            Q(supervisor_operation_id__icontains=search_query)

        )



    paginator = Paginator(all_deployments, page_size)

    try:
        paginated_deployments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_deployments = paginator.page(1)
    except EmptyPage:
        paginated_deployments = paginator.page(paginator.num_pages)

    all_deployments_serializer = AllDeploymentsSerializer(paginated_deployments, many=True)


    data['deployments'] = all_deployments_serializer.data
    data['pagination'] = {
        'page_number': paginated_deployments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_deployments.next_page_number() if paginated_deployments.has_next() else None,
        'previous': paginated_deployments.previous_page_number() if paginated_deployments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def deploy_team(request):
    payload = {}
    data = {}
    errors = {}

    deployment_id = request.data.get('deployment_id', "")

    if not deployment_id:
        errors['deployment_id'] = ["Deployment id required"]

    try:
        deployment = Deployment.objects.get(deployment_id=deployment_id)
    except Deployment.DoesNotExist:
        errors['deployment_id'] = ['Deployment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    deployment.deployed = True
    deployment.save()




    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



