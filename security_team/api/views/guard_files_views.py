from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from security_team.api.serializers import AllSecurityGuardsSerializer, AllGuardFilesSerializer
from security_team.models import SecurityGuard, SecurityGuardFile

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_guard_file_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_id = request.data.get('guard_id', "")
        file_name = request.data.get('file_name', "")
        file = request.data.get('file', "")


        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not file_name:
            errors['file_name'] = ['File name is required.']

        if not file:
            errors['file'] = ['File required.']


        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Security guard does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_guard_file = SecurityGuardFile.objects.create(
                guard=guard,
                file_name=file_name,
                file=file,
            )
        data['guard_file_id'] = new_guard_file.guard_file_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_guard_file_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_file_id = request.data.get('guard_file_id', "")
        guard_id = request.data.get('guard_id', "")
        file_name = request.data.get('file_name', "")
        file = request.data.get('file', "")


        if not guard_file_id:
            errors['guard_file_id'] = ['Guard File ID is required.']

        if not guard_id:
            errors['guard_id'] = ['Guard ID is required.']

        if not file_name:
            errors['file_name'] = ['File name is required.']

        if not file:
            errors['file'] = ['File required.']


        try:
            guard_file = SecurityGuardFile.objects.get(guard_file_id=guard_file_id)
        except:
            errors['guard_file_id'] = ['Guard File does not exist.']


        try:
            guard = SecurityGuard.objects.get(guard_id=guard_id)
        except:
            errors['guard_id'] = ['Security guard does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        guard_file.guard = guard
        guard_file.file_name = file_name
        guard_file.file = file
        guard_file.save()

        data['guard_file_id'] = guard_file.guard_file_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_guard_files_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_guard_files = SecurityGuardFile.objects.all().filter(is_archived=False)


    if search_query:
        all_guard_files = all_guard_files.filter(
            Q(file_name__icontains=search_query) |
            Q(guard_file_id__icontains=search_query)

        )


    paginator = Paginator(all_guard_files, page_size)

    try:
        paginated_guard_files = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_guard_files = paginator.page(1)
    except EmptyPage:
        paginated_guard_files = paginator.page(paginator.num_pages)

    all_guard_files_serializer = AllGuardFilesSerializer(paginated_guard_files, many=True)


    data['guard_files'] = all_guard_files_serializer.data
    data['pagination'] = {
        'page_number': paginated_guard_files.number,
        'total_pages': paginator.num_pages,
        'next': paginated_guard_files.next_page_number() if paginated_guard_files.has_next() else None,
        'previous': paginated_guard_files.previous_page_number() if paginated_guard_files.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_guard_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_file_id = request.data.get('guard_file_id', "")

        if not guard_file_id:
            errors['guard_file_id'] = ['Guard ID is required.']

        try:
            guard_file = SecurityGuardFile.objects.get(guard_file_id=guard_file_id)
        except:
            errors['guard_file_id'] = ['Guard file does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        guard_file.is_archived = True
        guard_file.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_guard_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_file_id = request.data.get('guard_file_id', "")

        if not guard_file_id:
            errors['guard_file_id'] = ['Guard ID is required.']

        try:
            guard_file = SecurityGuardFile.objects.get(guard_file_id=guard_file_id)
        except:
            errors['guard_file_id'] = ['Guard file does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        guard_file.is_archived = False
        guard_file.save()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_guard_file(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        guard_file_id = request.data.get('guard_file_id', "")

        if not guard_file_id:
            errors['guard_file_id'] = ['Guard ID is required.']

        try:
            guard_file = SecurityGuardFile.objects.get(guard_file_id=guard_file_id)
        except:
            errors['guard_file_id'] = ['Guard file does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        guard_file.delete()



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_guard_files_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_guard_files = SecurityGuardFile.objects.all().filter(is_archived=True)


    if search_query:
        all_guard_files = all_guard_files.filter(
            Q(file_name__icontains=search_query) |
            Q(guard_file_id__icontains=search_query)

        )


    paginator = Paginator(all_guard_files, page_size)

    try:
        paginated_guard_files = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_guard_files = paginator.page(1)
    except EmptyPage:
        paginated_guard_files = paginator.page(paginator.num_pages)

    all_guard_files_serializer = AllGuardFilesSerializer(paginated_guard_files, many=True)


    data['guard_files'] = all_guard_files_serializer.data
    data['pagination'] = {
        'page_number': paginated_guard_files.number,
        'total_pages': paginator.num_pages,
        'next': paginated_guard_files.next_page_number() if paginated_guard_files.has_next() else None,
        'previous': paginated_guard_files.previous_page_number() if paginated_guard_files.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

