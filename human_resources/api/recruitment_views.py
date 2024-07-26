
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email, check_email_exist
from activities.models import AllActivity
from human_resources.api.serializers import AllRecruitmentsSerializer, RecruitmentDetailsSerializer
from human_resources.models import Recruitment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_recruitment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone = request.data.get('phone', "")
        photo = request.data.get('photo', "")
        position = request.data.get('position', "")
        gender = request.data.get('gender', "")


        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email already exists in our database.']

        if not position:
            errors['position'] = ['Position is required.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        recruitment = Recruitment.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            position=position,
            gender=gender,
            phone=phone,
            photo=photo,

        )

        data["recruitment_id"] = recruitment.recruitment_id



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_recruitments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_recruitments = Recruitment.objects.all().filter(is_archived=False)


    if search_query:
        all_recruitments = all_recruitments.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(phone__icontains=search_query)

        )


    paginator = Paginator(all_recruitments, page_size)

    try:
        paginated_recruitments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_recruitments = paginator.page(1)
    except EmptyPage:
        paginated_recruitments = paginator.page(paginator.num_pages)

    all_recruitments_serializer = AllRecruitmentsSerializer(paginated_recruitments, many=True)


    data['recruitments'] = all_recruitments_serializer.data
    data['pagination'] = {
        'page_number': paginated_recruitments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_recruitments.next_page_number() if paginated_recruitments.has_next() else None,
        'previous': paginated_recruitments.previous_page_number() if paginated_recruitments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_recruitment_details_view(request):
    payload = {}
    data = {}
    errors = {}

    recruitment_id = request.query_params.get('recruitment_id', None)

    if not recruitment_id:
        errors['recruitment_id'] = ["Recruitment id required"]

    try:
        recruitment = Recruitment.objects.get(recruitment_id=recruitment_id)
    except Recruitment.DoesNotExist:
        errors['recruitment_id'] = ['Recruitment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    recruitment_serializer = RecruitmentDetailsSerializer(recruitment, many=False)
    if recruitment_serializer:
        recruitment = recruitment_serializer.data


    payload['message'] = "Successful"
    payload['data'] = recruitment

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_recruitment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        recruitment_id = request.data.get('recruitment_id', "")
        email = request.data.get('email', "").lower()
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        phone = request.data.get('phone', "")
        dob = request.data.get('dob', "")
        photo = request.data.get('photo', "")
        position = request.data.get('position', "")
        gender = request.data.get('gender', "")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email already exists in our database.']

        if not position:
            errors['position'] = ['Position is required.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        try:
            recruitment = Recruitment.objects.get(recruitment_id=recruitment_id)
        except:
            errors['recruitment_id'] = ['Recruitment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment.email = email
        recruitment.first_name = first_name
        recruitment.last_name = last_name
        recruitment.gender = gender
        recruitment.photo = photo
        recruitment.phone = phone
        recruitment.position = position

        recruitment.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_recruitment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        recruitment_id = request.data.get('recruitment_id', "")

        if not recruitment_id:
            errors['recruitment_id'] = ['Recruitment ID is required.']

        try:
            recruitment = Recruitment.objects.get(recruitment_id=recruitment_id)
        except:
            errors['recruitment_id'] = ['Recruitment does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment.is_archived = True
        recruitment.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_recruitment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        recruitment_id = request.data.get('recruitment_id', "")

        if not recruitment_id:
            errors['recruitment_id'] = ['Recruitment ID is required.']

        try:
            recruitment = Recruitment.objects.get(recruitment_id=recruitment_id)
        except:
            errors['recruitment_id'] = ['Recruitment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_recruitment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        recruitment_id = request.data.get('recruitment_id', "")

        if not recruitment_id:
            errors['recruitment_id'] = ['Recruitment ID is required.']

        try:
            recruitment = Recruitment.objects.get(recruitment_id=recruitment_id)
        except:
            errors['recruitment_id'] = ['Recruitment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment.is_archived = False
        recruitment.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_recruitments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_recruitments = Recruitment.objects.all().filter(is_archived=True)


    if search_query:
        all_recruitments = all_recruitments.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(phone__icontains=search_query)

        )


    paginator = Paginator(all_recruitments, page_size)

    try:
        paginated_recruitments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_recruitments = paginator.page(1)
    except EmptyPage:
        paginated_recruitments = paginator.page(paginator.num_pages)

    all_recruitments_serializer = AllRecruitmentsSerializer(paginated_recruitments, many=True)


    data['recruitments'] = all_recruitments_serializer.data
    data['pagination'] = {
        'page_number': paginated_recruitments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_recruitments.next_page_number() if paginated_recruitments.has_next() else None,
        'previous': paginated_recruitments.previous_page_number() if paginated_recruitments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

