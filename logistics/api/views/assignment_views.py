
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email
from logistics.api.serializers import AllAssignmentSerializer, AssignmentDetailsSerializer
from logistics.models import Assignment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_assignment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()
        name = request.data.get('name', "")
        phone_number = request.data.get('phone_number', "")
        address = request.data.get('address', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']

        if not name:
            errors['name'] = ['Name is required.']

        if not phone_number:
            errors['phone_number'] = ['Phone is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_assignment = Assignment.objects.create(
            name=name,
            phone_number=phone_number,
            email=email,
            address=address
        )



        data["assignment_id"] = new_assignment.assignment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_assignment_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_assignments = Assignment.objects.all().filter(is_archived=False)


    if search_query:
        all_assignments = all_assignments.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email_number__icontains=search_query) |
            Q(address_number__icontains=search_query)
        )


    paginator = Paginator(all_assignments, page_size)

    try:
        paginated_assignments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_assignments = paginator.page(1)
    except EmptyPage:
        paginated_assignments = paginator.page(paginator.num_pages)

    all_assignments_serializer = AllAssignmentSerializer(paginated_assignments, many=True)


    data['assignments'] = all_assignments_serializer.data
    data['pagination'] = {
        'page_number': paginated_assignments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_assignments.next_page_number() if paginated_assignments.has_next() else None,
        'previous': paginated_assignments.previous_page_number() if paginated_assignments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_assignment_details_view(request):
    payload = {}
    data = {}
    errors = {}

    assignment_id = request.query_params.get('assignment_id', None)

    if not assignment_id:
        errors['assignment_id'] = ["Assignment id required"]

    try:
        assignment = Assignment.objects.get(assignment_id=assignment_id)
    except:
        errors['assignment_id'] = ['Assignment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    assignment_serializer = AssignmentDetailsSerializer(assignment, many=False)
    if assignment_serializer:
        assignment = assignment_serializer.data


    payload['message'] = "Successful"
    payload['data'] = assignment

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_assignment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        assignment_id = request.data.get('assignment_id', "")

        email = request.data.get('email', "").lower()
        name = request.data.get('name', "")
        phone_number = request.data.get('phone_number', "")
        address = request.data.get('address', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']

        if not name:
            errors['name'] = ['Name is required.']

        if not phone_number:
            errors['phone_number'] = ['Phone is required.']

        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
        except:
            errors['assignment_id'] = ['Assignment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        assignment.name = name
        assignment.phone_number = phone_number
        assignment.email = email
        assignment.address = address
        assignment.save()

        data["assignment_id"] = assignment.assignment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_assignment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        assignment_id = request.data.get('assignment_id', "")

        if not assignment_id:
            errors['assignment_id'] = ['Assignment ID is required.']

        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
        except:
            errors['assignment_id'] = ['Assignment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        assignment.is_archived = True
        assignment.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_assignment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        assignment_id = request.data.get('assignment_id', "")

        if not assignment_id:
            errors['assignment_id'] = ['Assignment ID is required.']

        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
        except:
            errors['assignment_id'] = ['Assignment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        assignment.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_assignment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        assignment_id = request.data.get('assignment_id', "")

        if not assignment_id:
            errors['assignment_id'] = ['Assignment ID is required.']

        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
        except:
            errors['assignment_id'] = ['Assignment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        assignment.is_archived = False
        assignment.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_assignments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_assignments = Assignment.objects.all().filter(is_archived=True)


    if search_query:
        all_assignments = all_assignments.filter(
            Q(name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email_number__icontains=search_query) |
            Q(address_number__icontains=search_query)


        )




    paginator = Paginator(all_assignments, page_size)

    try:
        paginated_assignments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_assignments = paginator.page(1)
    except EmptyPage:
        paginated_assignments = paginator.page(paginator.num_pages)

    all_assignments_serializer = AllAssignmentSerializer(paginated_assignments, many=True)


    data['assignments'] = all_assignments_serializer.data
    data['pagination'] = {
        'page_number': paginated_assignments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_assignments.next_page_number() if paginated_assignments.has_next() else None,
        'previous': paginated_assignments.previous_page_number() if paginated_assignments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


