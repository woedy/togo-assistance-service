from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import get_template
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.custom_jwt import CustomJWTAuthentication
from bookings.api.serializers import AllBookingEmailsSerializer
from bookings.models import Booking, BookingEmail


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def send_booking_email(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        title = request.data.get('title', "")
        message = request.data.get('message', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not title:
            errors['title'] = ['Title is required.']

        if not message:
            errors['message'] = ['Message is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking_email = BookingEmail.objects.create(
                booking=booking,
                title=title,
                message=message,

            )


        context = {
            'email': booking.client.user.email,
            'first_name': booking.client.user.first_name,
            'last_name': booking.client.user.last_name,
            'company_name': booking.client.company_name,
            'subject': title,
            'message': message,
        }

        txt_ = get_template("booking/emails/booking_email.html").render(context)
        html_ = get_template("booking/emails/booking_email.txt").render(context)

        subject = title
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [booking.client.user.email]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        # )
        # # Execute the Celery chain asynchronously
        # email_chain.apply_async()

        send_mail(
            subject,
            txt_,
            from_email,
            recipient_list,
            html_message=html_,
            fail_silently=False,
        )




        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_booking_emails_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    booking_id = request.query_params.get('booking_id', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_booking_emails = BookingEmail.objects.all().filter(is_archived=False)


    if search_query:
        all_booking_emails = all_booking_emails.filter(
            Q(title__icontains=search_query) |
            Q(booking_booking_id__icontains=search_query)
        )



    if booking_id:
        all_booking_emails = all_booking_emails.filter(
            Q(booking_booking_id__icontains=booking_id)
        )


    paginator = Paginator(all_booking_emails, page_size)

    try:
        paginated_booking_emails = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_booking_emails = paginator.page(1)
    except EmptyPage:
        paginated_booking_emails = paginator.page(paginator.num_pages)

    all_booking_emails_serializer = AllBookingEmailsSerializer(paginated_booking_emails, many=True)


    data['booking_emails'] = all_booking_emails_serializer.data
    data['pagination'] = {
        'page_number': paginated_booking_emails.number,
        'total_pages': paginator.num_pages,
        'next': paginated_booking_emails.next_page_number() if paginated_booking_emails.has_next() else None,
        'previous': paginated_booking_emails.previous_page_number() if paginated_booking_emails.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)








@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_booking_email(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email_id = request.data.get('email_id', "")

        if not email_id:
            errors['email_id'] = ['Booking Email ID is required.']


        try:
            booking_email = BookingEmail.objects.get(id=email_id)
        except:
            errors['booking'] = ['Booking Email does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking_email.is_archived = True
        booking_email.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)







@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_booking_email(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email_id = request.data.get('email_id', "")

        if not email_id:
            errors['email_id'] = ['Booking Email ID is required.']


        try:
            booking_email = BookingEmail.objects.get(id=email_id)
        except:
            errors['booking'] = ['Booking Email does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking_email.is_archived = False
        booking_email.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_booking_email(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email_id = request.data.get('email_id', "")

        if not email_id:
            errors['email_id'] = ['Booking Email ID is required.']


        try:
            booking_email = BookingEmail.objects.get(id=email_id)
        except:
            errors['booking'] = ['Booking Email does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        booking_email.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)







@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archived_booking_emails_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    booking_id = request.query_params.get('booking_id', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_booking_emails = BookingEmail.objects.all().filter(is_archived=True)


    if search_query:
        all_booking_emails = all_booking_emails.filter(
            Q(title__icontains=search_query) |
            Q(booking_booking_id__icontains=search_query)
        )



    if booking_id:
        all_booking_emails = all_booking_emails.filter(
            Q(booking_booking_id__icontains=booking_id)
        )


    paginator = Paginator(all_booking_emails, page_size)

    try:
        paginated_booking_emails = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_booking_emails = paginator.page(1)
    except EmptyPage:
        paginated_booking_emails = paginator.page(paginator.num_pages)

    all_booking_emails_serializer = AllBookingEmailsSerializer(paginated_booking_emails, many=True)


    data['booking_emails'] = all_booking_emails_serializer.data
    data['pagination'] = {
        'page_number': paginated_booking_emails.number,
        'total_pages': paginator.num_pages,
        'next': paginated_booking_emails.next_page_number() if paginated_booking_emails.has_next() else None,
        'previous': paginated_booking_emails.previous_page_number() if paginated_booking_emails.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)






