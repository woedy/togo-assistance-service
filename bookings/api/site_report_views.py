
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.api.serializers import AllSiteReportsSerializer, SiteReportDetailsSerializer

from post_sites.models import ClientPostSite, SiteReport

User = get_user_model()


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_site_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_id = request.data.get('site_id', "")
        subject = request.data.get('subject', "")
        description = request.data.get('description', "")
        sender_id = request.data.get('sender_id', "")


        if not site_id:
            errors['site_id'] = ['Post Site ID is required.']

        if not subject:
            errors['subject'] = ['Subject is required.']

        if not description:
            errors['description'] = ['Description is required.']

        if not sender_id:
            errors['sender_id'] = ['Sender user id is required.']


        try:
            post_site = ClientPostSite.objects.get(site_id=site_id)
        except:
            errors['site_id'] = ['Post Site does not exist.']



        try:
            sender = User.objects.get(user_id=sender_id)
        except:
            errors['sender_id'] = ['User Does not exist does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        site_report = SiteReport.objects.create(
            post_site=post_site,
            subject=subject,
            description=description,
            sender=sender
        )

        data["site_report_id"] = site_report.site_report_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_site_reports_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_site_reports = SiteReport.objects.all().filter(is_archived=False)


    if search_query:
        all_site_reports = all_site_reports.filter(
            Q(site_report_id__icontains=search_query) |
            Q(subject__icontains=search_query)

        )


    paginator = Paginator(all_site_reports, page_size)

    try:
        paginated_site_reports = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_site_reports = paginator.page(1)
    except EmptyPage:
        paginated_site_reports = paginator.page(paginator.num_pages)

    all_site_reports_serializer = AllSiteReportsSerializer(paginated_site_reports, many=True)


    data['site_reports'] = all_site_reports_serializer.data
    data['pagination'] = {
        'page_number': paginated_site_reports.number,
        'total_pages': paginator.num_pages,
        'next': paginated_site_reports.next_page_number() if paginated_site_reports.has_next() else None,
        'previous': paginated_site_reports.previous_page_number() if paginated_site_reports.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_site_report_details_view(request):
    payload = {}
    data = {}
    errors = {}

    site_report_id = request.query_params.get('site_report_id', None)

    if not site_report_id:
        errors['site_report_id'] = ["Site Report id required"]

    try:
        site_report = SiteReport.objects.get(site_report_id=site_report_id)
    except:
        errors['site_report_id'] = ['Site Report does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    site_report_serializer = SiteReportDetailsSerializer(site_report, many=False)
    if site_report_serializer:
        site_report = site_report_serializer.data


    payload['message'] = "Successful"
    payload['data'] = site_report

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_site_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_report_id = request.data.get('site_report_id', "")
        site_id = request.data.get('site_id', "")
        subject = request.data.get('subject', "")
        description = request.data.get('description', "")
        sender_id = request.data.get('sender_id', "")

        if not site_report_id:
            errors['site_report_id'] = ['Site Report ID is required.']


        if not site_id:
            errors['site_id'] = ['Post Site ID is required.']

        if not subject:
            errors['subject'] = ['Subject is required.']

        if not description:
            errors['description'] = ['Description is required.']

        try:
            post_site = ClientPostSite.objects.get(site_id=site_id)
        except:
            errors['site_id'] = ['Post Site does not exist.']


        try:
            site_report = SiteReport.objects.get(site_report_id=site_report_id)
        except:
            errors['site_report_id'] = ['Site Report does not exist.']




        try:
            sender = User.objects.get(user_id=sender_id)
        except:
            errors['sender_id'] = ['User Does not exist does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        site_report.subject = subject
        site_report.description = description
        site_report.post_site = post_site
        site_report.sender = sender

        site_report.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_site_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_report_id = request.data.get('site_report_id', "")

        if not site_report_id:
            errors['site_report_id'] = ['Site Report ID is required.']

        try:
            site_report = SiteReport.objects.get(site_report_id=site_report_id)
        except:
            errors['site_report_id'] = ['Site Report does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        site_report.is_archived = True
        site_report.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_site_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_report_id = request.data.get('site_report_id', "")

        if not site_report_id:
            errors['site_report_id'] = ['Site Report ID is required.']

        try:
            site_report = SiteReport.objects.get(site_report_id=site_report_id)
        except:
            errors['site_report_id'] = ['Site Report does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        site_report.is_archived = False
        site_report.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_site_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        site_report_id = request.data.get('site_report_id', "")

        if not site_report_id:
            errors['site_report_id'] = ['Site Report ID is required.']

        try:
            site_report = SiteReport.objects.get(site_report_id=site_report_id)
        except:
            errors['site_report_id'] = ['Site Report does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        site_report.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_unarchived_site_reports_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_site_reports = SiteReport.objects.all().filter(is_archived=True)


    if search_query:
        all_site_reports = all_site_reports.filter(
            Q(site_report_id__icontains=search_query) |
            Q(subject__icontains=search_query)

        )


    paginator = Paginator(all_site_reports, page_size)

    try:
        paginated_site_reports = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_site_reports = paginator.page(1)
    except EmptyPage:
        paginated_site_reports = paginator.page(paginator.num_pages)

    all_site_reports_serializer = AllSiteReportsSerializer(paginated_site_reports, many=True)


    data['site_reports'] = all_site_reports_serializer.data
    data['pagination'] = {
        'page_number': paginated_site_reports.number,
        'total_pages': paginator.num_pages,
        'next': paginated_site_reports.next_page_number() if paginated_site_reports.has_next() else None,
        'previous': paginated_site_reports.previous_page_number() if paginated_site_reports.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

