
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from accounts.api.views import is_valid_email, check_email_exist
from human_resources.api.serializers import AllRecruitmentAttachmentsSerializer, RecruitmentAttachmentDetailsSerializer
from human_resources.models import Recruitment, RecruitmentAttachment

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_recruitment_attachment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        recruitment_id = request.data.get('recruitment_id', "")
        file = request.data.get('file', "")
        file_name = request.data.get('file_name', "")
        description = request.data.get('description', "")



        if not recruitment_id:
            errors['recruitment_id'] = ['Recruitment ID is required.']

        if not file:
            errors['file'] = ['File is required.']

        if not file_name:
            errors['file_name'] = ['File name is required.']

        if not description:
            errors['description'] = ['Description is required.']


        try:
            recruitment = Recruitment.objects.get(recruitment_id=recruitment_id)
        except:
            errors['recruitment_id'] = ['Recruitment does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        recruitment_attachment = RecruitmentAttachment.objects.create(
            recruitment=recruitment,
            file=file,
            file_name=file_name,
            description=description,

        )

        data["id"] = recruitment_attachment.id



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_recruitment_attachments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_recruitment_attachments = RecruitmentAttachment.objects.all().filter(is_archived=False)


    if search_query:
        all_recruitment_attachments = all_recruitment_attachments.filter(
            Q(file_name__icontains=search_query) |
            Q(recruitment_recruitment_id__icontains=search_query)

        )


    paginator = Paginator(all_recruitment_attachments, page_size)

    try:
        paginated_recruitment_attachments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_recruitment_attachments = paginator.page(1)
    except EmptyPage:
        paginated_recruitment_attachments = paginator.page(paginator.num_pages)

    all_recruitment_attachments_serializer = AllRecruitmentAttachmentsSerializer(paginated_recruitment_attachments, many=True)


    data['recruitment_attachments'] = all_recruitment_attachments_serializer.data
    data['pagination'] = {
        'page_number': paginated_recruitment_attachments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_recruitment_attachments.next_page_number() if paginated_recruitment_attachments.has_next() else None,
        'previous': paginated_recruitment_attachments.previous_page_number() if paginated_recruitment_attachments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_recruitment_attachment_details_view(request):
    payload = {}
    data = {}
    errors = {}

    id = request.query_params.get('id', None)

    if not id:
        errors['id'] = ["Recruitment attachment id required"]

    try:
        recruitment_attachment = RecruitmentAttachment.objects.get(id=id)
    except RecruitmentAttachment.DoesNotExist:
        errors['id'] = ['Recruitment Attachment does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    recruitment_attachment_serializer = RecruitmentAttachmentDetailsSerializer(recruitment_attachment, many=False)
    if recruitment_attachment_serializer:
        recruitment_attachment = recruitment_attachment_serializer.data


    payload['message'] = "Successful"
    payload['data'] = recruitment_attachment

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_recruitment_attachment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['Recruitment Attachment ID is required.']

        try:
            recruitment_attachment = RecruitmentAttachment.objects.get(id=id)
        except:
            errors['id'] = ['Recruitment Attachment does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment_attachment.is_archived = True
        recruitment_attachment.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_recruitment_attachment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['Recruitment Attachment ID is required.']

        try:
            recruitment_attachment = RecruitmentAttachment.objects.get(id=id)
        except:
            errors['id'] = ['Recruitment Attachment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment_attachment.is_archived = False
        recruitment_attachment.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_recruitment_attachment(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        id = request.data.get('id', "")

        if not id:
            errors['id'] = ['Recruitment Attachment ID is required.']

        try:
            recruitment_attachment = RecruitmentAttachment.objects.get(id=id)
        except:
            errors['id'] = ['Recruitment Attachment does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        recruitment_attachment.delete()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_recruitment_attachments_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_recruitment_attachments = RecruitmentAttachment.objects.all().filter(is_archived=True)


    if search_query:
        all_recruitment_attachments = all_recruitment_attachments.filter(
            Q(file_name__icontains=search_query) |
            Q(recruitment_recruitment_id__icontains=search_query)

        )


    paginator = Paginator(all_recruitment_attachments, page_size)

    try:
        paginated_recruitment_attachments = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_recruitment_attachments = paginator.page(1)
    except EmptyPage:
        paginated_recruitment_attachments = paginator.page(paginator.num_pages)

    all_recruitment_attachments_serializer = AllRecruitmentAttachmentsSerializer(paginated_recruitment_attachments, many=True)


    data['recruitment_attachments'] = all_recruitment_attachments_serializer.data
    data['pagination'] = {
        'page_number': paginated_recruitment_attachments.number,
        'total_pages': paginator.num_pages,
        'next': paginated_recruitment_attachments.next_page_number() if paginated_recruitment_attachments.has_next() else None,
        'previous': paginated_recruitment_attachments.previous_page_number() if paginated_recruitment_attachments.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

