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
from bookings.models import Booking, Estimate, TaxSetting
from commercial.api.serializers import AllEstimatesSerializer
from commercial.models import Commercial
from operations.models import Operation


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_estimate_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        item = request.data.get('item', "")
        quantity = request.data.get('quantity', "")
        tax = request.data.get('tax', "")
        amount = request.data.get('amount', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not item:
            errors['item'] = ['Item required.']

        if not quantity:
            errors['quantity'] = ['Item quantity required.']

        if not amount:
            errors['amount'] = ['Amount required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_estimate = Estimate.objects.create(
                booking=booking,
                item=item,
                quantity=quantity,
                tax=tax,
                amount=amount,
            )

        data['estimate_id'] = new_estimate.estimate_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def send_estimate_to_client(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        commercial_id = request.data.get('commercial_id', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not commercial_id:
            errors['commercial_id'] = ['Commercial ID is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']
        try:
            commercial = Commercial.objects.get(commercial_id=commercial_id)
        except:
            errors['commercial_id'] = ['Commercial does not exist.']

        try:
            estimate = Estimate.objects.get(booking=booking)
        except:
            errors['estimate_id'] = ['Estimate does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        estimate.status = "Sent"
        #estimate.estimator = commercial
        estimate.save()






        context = {
            'booking_id': booking.booking_id,
            'estimate_id': estimate.estimate_id,
            'item': estimate.item,
            'quantity': estimate.quantity,
            'tax': estimate.tax,
            'email': booking.client.user.email,
            'first_name': booking.client.user.first_name,
            'last_name': booking.client.user.last_name
        }

        txt_ = get_template("commercial/emails/send_estimate.html").render(context)
        html_ = get_template("commercial/emails/send_estimate.txt").render(context)

        subject = 'REQUEST ESTIMATE'
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
def get_all_client_estimates(request):
    payload = {}
    data = {}
    errors = {}


    search_query = request.query_params.get('search', '')
    booking_id = request.query_params.get('booking_id', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if not booking_id:
        errors['booking_id'] = ['Booking ID is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    all_estimates = Estimate.objects.all().filter(is_archived=False, booking=booking, accepted=False).order_by('-created_at')


    if search_query:
        all_estimates = all_estimates.filter(
            Q(estimate_id__icontains=search_query)
        )


    paginator = Paginator(all_estimates, page_size)

    try:
        paginated_estimates = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_estimates = paginator.page(1)
    except EmptyPage:
        paginated_estimates = paginator.page(paginator.num_pages)

    all_estimates_serializer = AllEstimatesSerializer(paginated_estimates, many=True)


    data['estimates'] = all_estimates_serializer.data
    data['pagination'] = {
        'page_number': paginated_estimates.number,
        'total_pages': paginator.num_pages,
        'next': paginated_estimates.next_page_number() if paginated_estimates.has_next() else None,
        'previous': paginated_estimates.previous_page_number() if paginated_estimates.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_client_invoices(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    booking_id = request.query_params.get('booking_id', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    if not booking_id:
        errors['booking_id'] = ['Booking ID is required.']

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except:
        errors['booking_id'] = ['Booking does not exist.']

    all_estimates = Estimate.objects.all().filter(is_archived=False, booking=booking, accepted=True).order_by('-created_at')


    if search_query:
        all_estimates = all_estimates.filter(
            Q(estimate_id__icontains=search_query)
        )


    paginator = Paginator(all_estimates, page_size)

    try:
        paginated_estimates = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_estimates = paginator.page(1)
    except EmptyPage:
        paginated_estimates = paginator.page(paginator.num_pages)

    all_estimates_serializer = AllEstimatesSerializer(paginated_estimates, many=True)


    data['invoice'] = all_estimates_serializer.data
    data['pagination'] = {
        'page_number': paginated_estimates.number,
        'total_pages': paginator.num_pages,
        'next': paginated_estimates.next_page_number() if paginated_estimates.has_next() else None,
        'previous': paginated_estimates.previous_page_number() if paginated_estimates.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_estimate(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        estimate_id = request.data.get('estimate_id', "")

        if not estimate_id:
            errors['estimate_id'] = ['Estimate ID is required.']

        try:
            estimate = Estimate.objects.get(estimate_id=estimate_id)
        except:
            errors['estimate_id'] = ['Estimate does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        estimate.is_archived = True
        estimate.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_estimate(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        estimate_id = request.data.get('estimate_id', "")

        if not estimate_id:
            errors['estimate_id'] = ['Estimate ID is required.']

        try:
            estimate = Estimate.objects.get(estimate_id=estimate_id)
        except:
            errors['estimate_id'] = ['Estimate does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        estimate.is_archived = False
        estimate.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_estimate(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        estimate_id = request.data.get('estimate_id', "")

        if not estimate_id:
            errors['estimate_id'] = ['Estimate ID is required.']

        try:
            estimate = Estimate.objects.get(estimate_id=estimate_id)
        except:
            errors['estimate_id'] = ['Estimate does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        estimate.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_tax_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':

        tax = request.data.get('tax', "")


        if not tax:
            errors['tax'] = ['Tax amount is required.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        new_tax = TaxSetting.objects.create(
                tax=tax,
            )

        data['tax_id'] = new_tax.id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_tax_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'GET':
        try:

            tax = TaxSetting.objects.all().order_by('created_at').first()         
            tax_amount = tax.tax
            data['tax'] = tax_amount


        except:
            errors['tax'] = ['No tax available. set a new one.']

        
        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

 

        #print(tax)



        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_tax_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        tax_id = request.data.get('tax_id', "")

        if not tax_id:
            errors['tax_id'] = ['Task ID is required.']

        try:
            tax = TaxSetting.objects.get(id=tax_id)
        except:
            errors['tax_id'] = ['Tax does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        
        tax.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


