from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.api.serializers import AllFieldReportsSerializer, FieldReportDetailsSerializer
from bookings.models import FieldReport, Booking
from notifications.models import Notification


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_field_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        title = request.data.get('title', "")
        report = request.data.get('report', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not title:
            errors['title'] = ['Title is required.']

        if not report:
            errors['report'] = ['Report is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        try:
            report = FieldReport.objects.get(booking=booking)
            errors['booking_id'] = ['Field Report already exist. Update it']
        except:

            _report = FieldReport.objects.create(
                booking=booking,
                title=title,
                report=report,

            )

            notification = Notification.objects.create(
                english_title='Field Report Added',
                french_title='Rapport de terrain ajouté',
                english_subject="A new field report for " + booking.client.company_name + " has been added. Check and give it the necessary attention.",
                french_subject="Un nouveau rapport de terrain pour " + booking.client.company_name + " a été ajouté. Veuillez vérifier et lui accorder l'attention nécessaire.",
                department="COMMERCIAL"
            )

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)




        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_field_reports_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    filter_field_report = request.query_params.get('filter_field_report', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_field_reports = FieldReport.objects.all().filter(is_archived=False)


    if search_query:
        all_field_reports = all_field_reports.filter(
            Q(booking_booking_id__icontains=search_query)
        )



    if filter_field_report:
        all_field_reports = all_field_reports.filter(
            Q(booking_booking_id__icontains=filter_field_report)
        )


    paginator = Paginator(all_field_reports, page_size)

    try:
        paginated_reports = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_reports = paginator.page(1)
    except EmptyPage:
        paginated_reports = paginator.page(paginator.num_pages)

    all_reports_serializer = AllFieldReportsSerializer(paginated_reports, many=True)


    data['field_reports'] = all_reports_serializer.data
    data['pagination'] = {
        'page_number': paginated_reports.number,
        'total_pages': paginator.num_pages,
        'next': paginated_reports.next_page_number() if paginated_reports.has_next() else None,
        'previous': paginated_reports.previous_page_number() if paginated_reports.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_field_report_details_view(request):
    payload = {}
    data = {}
    errors = {}

    booking_id = request.query_params.get('booking_id', None)

    if not booking_id:
        errors['booking_id'] = ["Booking id required"]

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    try:
        field_report = FieldReport.objects.get(booking=booking)
    except:
        errors['booking_id'] = ['Field report does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)



    field_report_serializer = FieldReportDetailsSerializer(field_report, many=False)
    if field_report_serializer:
        report = field_report_serializer.data


    payload['message'] = "Successful"
    payload['data'] = report

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_field_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        title = request.data.get('title', "")
        report = request.data.get('report', "")


        if not title:
            errors['title'] = ['Title is required.']

        if not report:
            errors['report'] = ['Report is required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking'] = ['Bookingdoes not exist.']

        try:
            field_report = FieldReport.objects.get(booking=booking)
        except:
            errors['booking'] = ['Field report does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        field_report.title = title
        field_report.report = report
        field_report.save()

        notification = Notification.objects.create(
            english_title='Field Report Edited',
            french_title='Rapport de terrain modifié',
            english_subject="Field report for " + booking.client.company_name + " has been edited. Check and give it the necessary attention.",
            french_subject="Le rapport de terrain pour " + booking.client.company_name + " a été modifié. Veuillez vérifier et lui accorder l'attention nécessaire.",
            department="COMMERCIAL"
        )

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_field_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking'] = ['Bookingdoes not exist.']

        try:
            field_report = FieldReport.objects.get(booking=booking)
        except:
            errors['booking'] = ['Field report does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        field_report.is_archived = True
        field_report.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_field_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking'] = ['Bookingdoes not exist.']

        try:
            field_report = FieldReport.objects.get(booking=booking)
        except:
            errors['booking'] = ['Field report does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        field_report.is_archived = False
        field_report.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_field_report(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")

        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking'] = ['Bookingdoes not exist.']

        try:
            field_report = FieldReport.objects.get(booking=booking)
        except:
            errors['booking'] = ['Field report does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        field_report.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_field_reports_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    filter_field_report = request.query_params.get('filter_field_report', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_field_reports = FieldReport.objects.all().filter(is_archived=True)


    if search_query:
        all_field_reports = all_field_reports.filter(
            Q(booking_booking_id__icontains=search_query)
        )



    if filter_field_report:
        all_field_reports = all_field_reports.filter(
            Q(booking_booking_id__icontains=filter_field_report)
        )


    paginator = Paginator(all_field_reports, page_size)

    try:
        paginated_reports = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_reports = paginator.page(1)
    except EmptyPage:
        paginated_reports = paginator.page(paginator.num_pages)

    all_reports_serializer = AllFieldReportsSerializer(paginated_reports, many=True)


    data['field_reports'] = all_reports_serializer.data
    data['pagination'] = {
        'page_number': paginated_reports.number,
        'total_pages': paginator.num_pages,
        'next': paginated_reports.next_page_number() if paginated_reports.has_next() else None,
        'previous': paginated_reports.previous_page_number() if paginated_reports.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



