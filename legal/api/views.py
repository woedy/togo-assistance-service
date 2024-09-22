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
from commercial.api.serializers import AllEstimatesSerializer
from legal.api.serializers import AllContractsSerializer
from legal.models import Contract, Legal
from notifications.models import Notification


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def add_client_request_contract_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        file = request.data.get('file', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not file:
            errors['file'] = ['Contract file required.']


        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']

        try:
            contract = Contract.objects.get(booking=booking)
            errors['booking_id'] = ['Contract for this booking already exist. Update it.']
        except:
            new_contract = Contract.objects.create(
                booking=booking,
                file=file
            )

            notification = Notification.objects.create(
                english_title='New Contract Added',
                french_title='Nouveau contrat ajouté',
                english_subject="A new Contract for " + booking.client.company_name + " has been added. Check and give it the necessary attention.",
                french_subject="Un nouveau contrat pour " + booking.client.company_name + " a été ajouté. Veuillez vérifier et lui accorder l'attention nécessaire.",
                department="COMMERCIAL"
            )

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        data['contract_id'] = new_contract.contract_id


    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload)






@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def edit_client_request_contract_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        contract_id = request.data.get('contract_id', "")
        file = request.data.get('file', "")


        if not contract_id:
            errors['contract_id'] = ['Contract ID is required.']

        if not file:
            errors['file'] = ['Contract file required.']


        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except:
            errors['contract_id'] = ['Contract does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        contract.file = file
        contract.save()

        notification = Notification.objects.create(
            english_title='Contract Edited',
            french_title='Contrat modifié',
            english_subject="Contract for " + contract.booking.client.company_name + " has been edited. Check and give it the necessary attention.",
            french_subject="Le contrat de " + contract.booking.client.company_name + " a été modifié. Veuillez vérifier et lui accorder l'attention nécessaire.",
            department="COMMERCIAL"
        )


        data['contract_id'] = contract.contract_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def change_contract_status_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        contract_id = request.data.get('contract_id', "")
        _status = request.data.get('status', "")


        if not contract_id:
            errors['contract_id'] = ['Contract ID is required.']

        if not _status:
            errors['status'] = ['Status is required.']


        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except:
            errors['contract_id'] = ['Contract does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        contract.status = _status
        contract.save()

        #notification = Notification.objects.create(
        #    english_title='Contract Edited',
        #    french_title='Contrat modifié',
        #    english_subject="Contract for " + contract.booking.client.company_name + " has been edited. Check and give it the necessary attention.",
        #    french_subject="Le contrat de " + contract.booking.client.company_name + " a été modifié. Veuillez vérifier et lui accorder l'attention nécessaire.",
        #    department="COMMERCIAL"
        #)



        context = {
            'email': contract.booking.client.user.email,
            'first_name': contract.booking.client.user.first_name,
            'last_name': contract.booking.client.user.last_name,
            'company_name': contract.booking.client.company_name,
            'status': _status,
            'message': 'Message here',
        }

        txt_ = get_template("booking/contract/contract_status.html").render(context)
        html_ = get_template("booking/contract/contract_status.txt").render(context)

        subject = 'Contract Status Change'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [contract.booking.client.user.email]

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




        data['contract_id'] = contract.contract_id


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def send_contract_to_client(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        booking_id = request.data.get('booking_id', "")
        legal_id = request.data.get('legal_id', "")


        if not booking_id:
            errors['booking_id'] = ['Booking ID is required.']

        if not legal_id:
            errors['legal_id'] = ['Legal ID is required.']

        try:
            booking = Booking.objects.get(booking_id=booking_id)
        except:
            errors['booking_id'] = ['Booking does not exist.']
        try:
            legal = Legal.objects.get(legal_id=legal_id)
        except:
            errors['legal_id'] = ['Legal does not exist.']

        try:
            contract = Contract.objects.get(booking=booking)
        except:
            errors['contract_id'] = ['Contract does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        contract.status = "Sent"
        #contract.estimator = commercial
        contract.save()






        context = {
            'booking_id': booking.booking_id,
            'contract_id': contract.contract_id,
            'email': booking.client.user.email,
            'first_name': booking.client.user.first_name,
            'last_name': booking.client.user.last_name
        }

        txt_ = get_template("'commercial'/emails/send_contract.html").render(context)
        html_ = get_template("commercial/emails/send_contract.txt").render(context)

        subject = 'REQUEST CONTRACT'
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




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def sign_contract_to_client(request):
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
            errors['booking_id'] = ['Booking does not exist.']

        try:
            contract = Contract.objects.get(booking=booking)
        except:
            errors['contract_id'] = ['Contract does not exist.']



        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        contract.signed = True
        contract.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_client_contracts(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_contracts = Contract.objects.all().filter(is_archived=False)


    if search_query:
        all_contracts = all_contracts.filter(
            Q(contract_id__icontains=search_query)
        )


    paginator = Paginator(all_contracts, page_size)

    try:
        paginated_contracts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_contracts = paginator.page(1)
    except EmptyPage:
        paginated_contracts = paginator.page(paginator.num_pages)

    all_contracts_serializer = AllContractsSerializer(paginated_contracts, many=True)


    data['contracts'] = all_contracts_serializer.data
    data['pagination'] = {
        'page_number': paginated_contracts.number,
        'total_pages': paginator.num_pages,
        'next': paginated_contracts.next_page_number() if paginated_contracts.has_next() else None,
        'previous': paginated_contracts.previous_page_number() if paginated_contracts.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_contract(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        contract_id = request.data.get('contract_id', "")

        if not contract_id:
            errors['contract_id'] = ['Contract ID is required.']

        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except:
            errors['contract_id'] = ['Contract does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        contract.is_archived = True
        contract.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_contract(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        contract_id = request.data.get('contract_id', "")

        if not contract_id:
            errors['contract_id'] = ['Contract ID is required.']

        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except:
            errors['contract_id'] = ['Contract does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        contract.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_contract(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        contract_id = request.data.get('contract_id', "")

        if not contract_id:
            errors['contract_id'] = ['Contract ID is required.']

        try:
            contract = Contract.objects.get(contract_id=contract_id)
        except:
            errors['contract_id'] = ['Contract does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        contract.is_archived = False
        contract.save()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_all_archive_client_contracts(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10

    all_contracts = Contract.objects.all().filter(is_archived=True)


    if search_query:
        all_contracts = all_contracts.filter(
            Q(contract_id__icontains=search_query)
        )


    paginator = Paginator(all_contracts, page_size)

    try:
        paginated_contracts = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_contracts = paginator.page(1)
    except EmptyPage:
        paginated_contracts = paginator.page(paginator.num_pages)

    all_contracts_serializer = AllContractsSerializer(paginated_contracts, many=True)


    data['contracts'] = all_contracts_serializer.data
    data['pagination'] = {
        'page_number': paginated_contracts.number,
        'total_pages': paginator.num_pages,
        'next': paginated_contracts.next_page_number() if paginated_contracts.has_next() else None,
        'previous': paginated_contracts.previous_page_number() if paginated_contracts.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)







@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def list_deptors_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    page_size = 10


    all_estimates = Estimate.objects.all().filter(is_archived=False, accepted=True, paid=False).order_by('-created_at')


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


    data['deptors'] = all_estimates_serializer.data
    data['pagination'] = {
        'page_number': paginated_estimates.number,
        'total_pages': paginator.num_pages,
        'next': paginated_estimates.next_page_number() if paginated_estimates.has_next() else None,
        'previous': paginated_estimates.previous_page_number() if paginated_estimates.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)

