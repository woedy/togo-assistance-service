from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import get_template
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.models import Booking, Estimate
from legal.api.serializers import AllContractsSerializer
from legal.models import Contract, Legal
from secretary.api.serializers import AllFilesSerializer
from security_team.models import FileManagement


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_file_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        file_name = request.data.get('file_name', "")
        description = request.data.get('description', "")
        file = request.data.get('file', "")


        if not file_name:
            errors['file_name'] = ['File name is required.']

        if not file:
            errors['file'] = ['File required.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_file = FileManagement.objects.create(
            file=file,
            file_name=file_name,
            description=description
        )


        data['file_id'] = new_file.file_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_files(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_files = FileManagement.objects.all().filter(is_archived=False)


    if search_query:
        all_files = all_files.filter(
            Q(file_id__icontains=search_query) |
            Q(file_name__icontains=search_query)
        )


    paginator = Paginator(all_files, page_size)

    try:
        paginated_files = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_files = paginator.page(1)
    except EmptyPage:
        paginated_files = paginator.page(paginator.num_pages)

    all_files_serializer = AllFilesSerializer(paginated_files, many=True)


    data['files'] = all_files_serializer.data
    data['pagination'] = {
        'page_number': paginated_files.number,
        'total_pages': paginator.num_pages,
        'next': paginated_files.next_page_number() if paginated_files.has_next() else None,
        'previous': paginated_files.previous_page_number() if paginated_files.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        file_id = request.data.get('file_id', "")

        if not file_id:
            errors['file_id'] = ['File ID is required.']

        try:
            file = FileManagement.objects.get(file_id=file_id)
        except:
            errors['file_id'] = ['File does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        file.is_archived = True
        file.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        file_id = request.data.get('file_id', "")

        if not file_id:
            errors['file_id'] = ['File ID is required.']

        try:
            file = FileManagement.objects.get(file_id=file_id)
        except:
            errors['file_id'] = ['File does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        file.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        file_id = request.data.get('file_id', "")

        if not file_id:
            errors['file_id'] = ['File ID is required.']

        try:
            file = FileManagement.objects.get(file_id=file_id)
        except:
            errors['file_id'] = ['File does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        file.is_archived = False
        file.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archive_files(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_files = FileManagement.objects.all().filter(is_archived=True)


    if search_query:
        all_files = all_files.filter(
            Q(file_id__icontains=search_query) |
            Q(file_name__icontains=search_query)
        )


    paginator = Paginator(all_files, page_size)

    try:
        paginated_files = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_files = paginator.page(1)
    except EmptyPage:
        paginated_files = paginator.page(paginator.num_pages)

    all_files_serializer = AllFilesSerializer(paginated_files, many=True)


    data['files'] = all_files_serializer.data
    data['pagination'] = {
        'page_number': paginated_files.number,
        'total_pages': paginator.num_pages,
        'next': paginated_files.next_page_number() if paginated_files.has_next() else None,
        'previous': paginated_files.previous_page_number() if paginated_files.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


