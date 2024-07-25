
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.serializers import AllUserFilesSerializer, UserFileDetailsSerializer
from accounts.api.views import is_valid_email, check_email_exist
from accounts.models import UserFile
from activities.models import AllActivity
from bookings.api.serializers import PostOrderDetailsSerializer, AllPostOrdersSerializer

from post_sites.models import ClientPostSite

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_user_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")
        file = request.data.get('file', "")
        file_name = request.data.get('file_name', "")
        description = request.data.get('description', "")


        if not user_id:
            errors['user_id'] = ['User ID is required.']

        if not file_name:
            errors['file_name'] = ['File name is required.']

        if not file:
            errors['file'] = ['File is required.']



        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        user_file = UserFile.objects.create(
            user=user,
            file_name=file_name,
            file=file,
            description=description,
        )

        data["id"] = user_file.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_user_files_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_user_files = UserFile.objects.all().filter(is_archived=False)


    if search_query:
        all_user_files = all_user_files.filter(
            Q(id__icontains=search_query) |
            Q(file_name__icontains=search_query)

        )


    paginator = Paginator(all_user_files, page_size)

    try:
        paginated_user_files = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_user_files = paginator.page(1)
    except EmptyPage:
        paginated_user_files = paginator.page(paginator.num_pages)

    all_user_files_serializer = AllUserFilesSerializer(paginated_user_files, many=True)


    data['user_files'] = all_user_files_serializer.data
    data['pagination'] = {
        'page_number': paginated_user_files.number,
        'total_pages': paginator.num_pages,
        'next': paginated_user_files.next_page_number() if paginated_user_files.has_next() else None,
        'previous': paginated_user_files.previous_page_number() if paginated_user_files.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_user_file_details_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.query_params.get('id', None)

    if not id:
        errors['id'] = ["User Fileid required"]

    try:
        user_file = UserFile.objects.get(id=id)
    except:
        errors['id'] = ['User File does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    user_file_serializer = UserFileDetailsSerializer(user_file, many=False)
    if user_file_serializer:
        user_file = user_file_serializer.data


    payload['message'] = "Successful"
    payload['data'] = user_file

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_user_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['User File ID is required.']

        try:
            user_file = UserFile.objects.get(id=id)
        except:
            errors['id'] = ['User File does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user_file.is_archived = True
        user_file.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_user_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['File ID is required.']

        try:
            user_file = UserFile.objects.get(id=id)
        except:
            errors['id'] = ['User File does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user_file.is_archived = False
        user_file.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_user_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['File ID is required.']

        try:
            user_file = UserFile.objects.get(id=id)
        except:
            errors['id'] = ['User File does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user_file.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)









@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_user_files_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_user_files = UserFile.objects.all().filter(is_archived=True)


    if search_query:
        all_user_files = all_user_files.filter(
            Q(id__icontains=search_query) |
            Q(file_name__icontains=search_query)

        )


    paginator = Paginator(all_user_files, page_size)

    try:
        paginated_user_files = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_user_files = paginator.page(1)
    except EmptyPage:
        paginated_user_files = paginator.page(paginator.num_pages)

    all_user_files_serializer = AllUserFilesSerializer(paginated_user_files, many=True)


    data['user_files'] = all_user_files_serializer.data
    data['pagination'] = {
        'page_number': paginated_user_files.number,
        'total_pages': paginator.num_pages,
        'next': paginated_user_files.next_page_number() if paginated_user_files.has_next() else None,
        'previous': paginated_user_files.previous_page_number() if paginated_user_files.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



