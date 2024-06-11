
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
from logistics.models import Assignment, Equipment
from security_team.models import SecurityGuard

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_assignment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        equipment_id = request.data.get('equipment_id', "")
        quantity = request.data.get('quantity', "")
        return_due_date = request.data.get('return_due_date', "")

        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']


        if not equipment_id:
            errors['equipment_id'] = ['Equipment ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        if not return_due_date:
            errors['return_due_date'] = ['Return due date is required.']


        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        new_assignment = Assignment.objects.create(
            guard=guard,
            equipment=equipment,
            quantity=quantity,
            return_due_date=return_due_date
        )



        data["assignment_id"] = new_assignment.assignment_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_assignments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_assignments = Assignment.objects.all().filter(is_archived=False)


    if search_query:
        all_assignments = all_assignments.filter(
            Q(guard__user_first_name__icontains=search_query) |
            Q(guard__user_last_name__icontains=search_query) |
            Q(equipment_name__icontains=search_query) |
            Q(quantity__icontains=search_query) |
            Q(return_due_date__icontains=search_query)
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
        guard_id = request.data.get('guard_id', "")
        equipment_id = request.data.get('equipment_id', "")
        quantity = request.data.get('quantity', "")
        return_due_date = request.data.get('return_due_date', "")

        if not assignment_id:
            errors['assignment_id'] = ['Assignment ID is required.']


        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']


        if not equipment_id:
            errors['equipment_id'] = ['Equipment ID is required.']

        if not quantity:
            errors['quantity'] = ['Quantity is required.']

        if not return_due_date:
            errors['return_due_date'] = ['Return due date is required.']


        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Guard does not exist.']

        try:
            equipment = Equipment.objects.get(equipment_id=equipment_id)
        except:
            errors['equipment_id'] = ['Equipment does not exist.']


        try:
            assignment = Assignment.objects.get(assignment_id=assignment_id)
        except:
            errors['assignment_id'] = ['Assignment does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        assignment.guard = guard
        assignment.equipment = equipment
        assignment.quantity = quantity
        assignment.return_due_date = return_due_date
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
            Q(guard__user_first_name__icontains=search_query) |
            Q(guard__user_last_name__icontains=search_query) |
            Q(equipment_name__icontains=search_query) |
            Q(quantity__icontains=search_query) |
            Q(return_due_date__icontains=search_query)
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


