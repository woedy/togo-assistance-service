import re
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.template.loader import get_template
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api.custom_jwt import CustomTokenObtainPairSerializer, CustomJWTAuthentication
from accounts.api.serializers import UserRegistrationSerializer, PasswordResetSerializer, ListAllUsersSerializer
from activities.models import AllActivity
from administrative.api.serializers import AdminDepartmentDetailsSerializer
from administrative.models import AdminDepartment
from billing.api.serializers import BillingDetailsSerializer
from billing.models import Billing
from clients.models import Client
from commercial.api.serializers import CommercialDetailsSerializer
from commercial.models import Commercial
from communications.models import PrivateChatRoom
from human_resources.api.serializers import HumanResourceDetailsSerializer
from human_resources.models import HumanResource
from legal.models import Legal
from operations.api.serializers import OperationsDetailsSerializer
from operations.models import Operation
from secretary.api.serializers import SecretaryDetailsSerializer
from secretary.models import Secretary
from security_team.api.serializers import SecurityGuardDetailsSerializer
from security_team.models import SecurityGuard
from tas_project.utils import generate_email_token, generate_random_otp_code

User = get_user_model()


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def register_user(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        email = request.data.get('email', "").lower()
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        department = request.data.get('department', "")
        phone = request.data.get('phone', "")
        photo = request.data.get('photo', "")
        #photo = request.FILES.get('photo')
        password = request.data.get('password', "Tas@123!_")
        password2 = request.data.get('password2', "Tas@123!_")

        if not email:
            errors['email'] = ['User Email is required.']
        elif not is_valid_email(email):
            errors['email'] = ['Valid email required.']
        elif check_email_exist(email):
            errors['email'] = ['Email already exists in our database.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        if not password:
            errors['password'] = ['Password is required.']

        if not password2:
            errors['password2'] = ['Password2 is required.']

        if password != password2:
            errors['password'] = ['Passwords dont match.']

        if not is_valid_password(password):
            errors['password'] = [
                'Password must be at least 8 characters long\n- Must include at least one uppercase letter,\n- One lowercase letter, one digit,\n- And one special character']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data["user_id"] = user.user_id
            data["email"] = user.email
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name

            room = PrivateChatRoom.objects.create(
                user=user
            )

            if department == "SECRETARY":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                secretary_profile = Secretary.objects.create(
                    user=user,
                    room=room
                )
                data["room_id"] = secretary_profile.room.room_id
                data["secretary_id"] = secretary_profile.secretary_id

            if department == "HUMAN RESOURCES":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                hr_profile = HumanResource.objects.create(
                    user=user,
                    room=room

                )
                data["room_id"] = hr_profile.room.room_id
                data["hr_id"] = hr_profile.hr_id

            if department == "ADMIN":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                admin_profile = AdminDepartment.objects.create(
                    user=user,
                    room=room
                )
                data["room_id"] = admin_profile.room.room_id
                data["admin_id"] = admin_profile.admin_id

            if department == "OPERATIONS":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                operations_profile = Operation.objects.create(
                    user=user,
                    room=room

                )
                data["room_id"] = operations_profile.room.room_id
                data["operations_id"] = operations_profile.operations_id

            if department == "COMMERCIAL":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                commercial_profile = Commercial.objects.create(
                    user=user,
                    room=room

                )
                data["room_id"] = commercial_profile.room.room_id
                data["commercial_id"] = commercial_profile.commercial_id

            if department == "BILLING":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                accounts_profile = Billing.objects.create(
                    user=user,
                    room=room

                )
                data["room_id"] = accounts_profile.room.room_id
                data["billing_id"] = accounts_profile.billing_id

            if department == "GUARD":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                guard_profile = SecurityGuard.objects.create(
                    user=user,
                    room=room

                )
                data["room_id"] = guard_profile.room.room_id
                data["guard_id"] = guard_profile.guard_id

            if department == "LEGAL":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                legal_profile = Legal.objects.create(
                    user=user,
                    room=room

                )
                data["room_id"] = legal_profile.room.room_id
                data["legal_id"] = legal_profile.legal_id


        # Generate token using the custom serializer
        serializer = CustomTokenObtainPairSerializer()
        _token = serializer.get_token(user)

        token = {
            'refresh': str(_token),
            'access': str(_token.access_token),
        }

        data['token'] = token

        email_token = generate_email_token()

        user = User.objects.get(email=email)
        user.email_token = email_token
        user.save()

        context = {
            'email_token': email_token,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }

        txt_ = get_template("registration/emails/verify.html").render(context)
        html_ = get_template("registration/emails/verify.txt").render(context)

        subject = 'EMAIL CONFIRMATION CODE'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

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

        #
        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Registration",
            body=user.email + " Just created an account."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)



@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def edit_profile(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':

        user_id = request.data.get('user_id', "")
        #email = request.data.get('email', "").lower()
        first_name = request.data.get('first_name', "")
        last_name = request.data.get('last_name', "")
        department = request.data.get('department', "")
        phone = request.data.get('phone', "")
        photo = request.FILES.get('photo')

        #if not email:
        #    errors['email'] = ['User Email is required.']
        #elif not is_valid_email(email):
        #    errors['email'] = ['Valid email required.']

        if not first_name:
            errors['first_name'] = ['First Name is required.']

        if not phone:
            errors['phone'] = ['Phone number is required.']

        if not last_name:
            errors['last_name'] = ['Last Name is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        if user:
            user.first_name = first_name
            user.last_name = last_name
            #user.email = email
            user.save()

            if department == "SECRETARY":
                user.department = department
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                try:
                    secretary_profile = Secretary.objects.get(
                    user=user,)
                except:
                    errors['user_id'] = ['Secretary does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                data["secretary_id"] = secretary_profile.secretary_id

            if department == "HUMAN RESOURCES":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                try:
                    hr_profile = HumanResource.objects.get(
                    user=user
                )
                except:
                    errors['user_id'] = ['Human Resource does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)


                data["hr_id"] = hr_profile.hr_id

            if department == "ADMIN":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone

                try:
                    admin_profile = AdminDepartment.objects.get(
                    user=user,
                )
                except:
                    errors['user_id'] = ['Admin Department does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)



                data["admin_id"] = admin_profile.admin_id

            if department == "OPERATIONS":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone
                try:
                    operations_profile = Operation.objects.get(
                    user=user,
                )
                except:
                    errors['user_id'] = ['Operations does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)


                data["operations_id"] = operations_profile.operations_id

            if department == "COMMERCIAL":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone
                try:
                    commercial_profile = Commercial.objects.get(
                    user=user,
                )
                except:
                    errors['user_id'] = ['Commercial does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                data["commercial_id"] = commercial_profile.commercial_id

            if department == "BILLING":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone
                try:
                    accounts_profile = Billing.objects.get(
                    user=user
                )
                except:
                    errors['user_id'] = ['Billing does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                data["billing_id"] = accounts_profile.billing_id

            if department == "GUARD":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone
                try:
                    guard_profile = SecurityGuard.objects.get(
                    user=user
                )
                except:
                    errors['user_id'] = ['Guard does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                data["guard_id"] = guard_profile.guard_id

            if department == "LEGAL":
                user.phone = phone
                user.photo = photo
                user.save()

                data["department"] = user.department
                data["photo"] = user.photo.url
                data["phone"] = user.phone
                try:
                    legal_profile = Legal.objects.get(
                    user=user
                )
                except:
                    errors['user_id'] = ['Legal does not exist.']

                if errors:
                    payload['message'] = "Errors"
                    payload['errors'] = errors
                    return Response(payload, status=status.HTTP_400_BAD_REQUEST)

                data["legal_id"] = legal_profile.legal_id

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)





@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def remove_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_deleted = True
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Removed",
            body=user.email + " Just deleted their account."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def verify_user_email(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    token_errors = []

    email = request.data.get('email', '').lower()
    email_token = request.data.get('email_token', '')

    if not email:
        email_errors.append('Email is required.')

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')

    if email_errors:
        errors['email'] = email_errors

    if not email_token:
        token_errors.append('Token is required.')

    user = None
    if qs.exists():
        user = qs.first()
        if email_token != user.email_token:
            token_errors.append('Invalid Token.')

    if token_errors:
        errors['email_token'] = token_errors

    if email_errors or token_errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    try:
        token = Token.objects.get(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    user.is_active = True
    user.email_verified = True
    user.save()

    data["user_id"] = user.user_id
    data["email"] = user.email

    payload['message'] = "Successful"
    payload['data'] = data

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Verify Email",
        body=user.email + " just verified their email",
    )
    new_activity.save()

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([AllowAny])
@authentication_classes([])
def resend_email_verification(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []

    email = request.data.get('email', '').lower()

    if not email:
        email_errors.append('Email is required.')
    if email_errors:
        errors['email'] = email_errors
        payload['message'] = "Error"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    otp_code = generate_email_token()
    user.email_token = otp_code
    user.save()

    context = {
        'email_token': otp_code,
        'email': user.email,
        'first_name': user.first_name
    }

    txt_ = get_template("registration/emails/verify.txt").render(context)
    html_ = get_template("registration/emails/verify.html").render(context)

    subject = 'OTP CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # # Use Celery chain to execute tasks in sequence
    # email_chain = chain(
    #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    #  )
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

    #data["otp_code"] = otp_code
    data["emai"] = user.email
    data["user_id"] = user.user_id

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Email verification sent",
        body="Email verification sent to " + user.email,
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)




class UserLogin(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = {}
        data = {}
        errors = {}

        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')
        fcm_token = request.data.get('fcm_token', '')

        if not email:
            errors['email'] = ['Email is required.']

        if not password:
            errors['password'] = ['Password is required.']

        if not fcm_token:
            errors['fcm_token'] = ['FCM device token is required.']

        try:
            qs = User.objects.filter(email=email)
        except User.DoesNotExist:
            errors['email'] = ['User does not exist.']

        if qs.exists():
            not_active = qs.filter(email_verified=False)
            if not_active:
                errors['email'] = ["Please check your email to confirm your account or resend confirmation email."]

        if not check_password(email, password):
            errors['password'] = ['Invalid Credentials']

        user = authenticate(email=email, password=password)

        if not user:
            errors['email'] = ['Invalid Credentials']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)


        # Generate token using the custom serializer
        serializer = CustomTokenObtainPairSerializer()
        _token = serializer.get_token(user)

        token = {
            'refresh': str(_token),
            'access': str(_token.access_token),
        }



        user.fcm_token = fcm_token
        user.save()

        data["user_id"] = user.user_id
        data["email"] = user.email
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["department"] = user.department
        data["phone"] = user.phone
        data["photo"] = user.photo.url
        data['token'] = token

        payload['message'] = "Successful"
        payload['data'] = data

        new_activity = AllActivity.objects.create(
            user=user,
            subject="User Login",
            body=user.email + " Just logged in."
        )
        new_activity.save()

        return Response(payload, status=status.HTTP_200_OK)


def check_password(email, password):
    try:
        user = User.objects.get(email=email)
        return user.check_password(password)
    except User.DoesNotExist:
        return False

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        payload = {}
        data = {}
        errors = {}
        email_errors = []

        email = request.data.get('email', '').lower()

        if not email:
            email_errors.append('Email is required.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

        qs = User.objects.filter(email=email)
        if not qs.exists():
            email_errors.append('Email does not exist.')
            if email_errors:
                errors['email'] = email_errors
                payload['message'] = "Error"
                payload['errors'] = errors
                return Response(payload, status=status.HTTP_404_NOT_FOUND)


        user = User.objects.filter(email=email).first()
        otp_code = generate_random_otp_code()
        user.otp_code = otp_code
        user.save()

        context = {
            'otp_code': otp_code,
            'email': user.email,
            'full_name': user.full_name
        }

        txt_ = get_template("registration/emails/send_otp.txt").render(context)
        html_ = get_template("registration/emails/send_otp.html").render(context)

        subject = 'OTP CODE'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user.email]

        # # Use Celery chain to execute tasks in sequence
        # email_chain = chain(
        #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
        #  )
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

        data["otp_code"] = otp_code
        data["email"] = user.email
        data["user_id"] = user.user_id

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Reset Password",
            body="OTP sent to " + user.email,
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

        return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def confirm_otp_password_view(request):
    payload = {}
    data = {}
    errors = {}

    email_errors = []
    otp_errors = []

    email = request.data.get('email', '').lower()
    otp_code = request.data.get('otp_code', '')

    if not email:
        email_errors.append('Email is required.')

    if not otp_code:
        otp_errors.append('OTP code is required.')

    user = User.objects.filter(email=email).first()

    if user is None:
        email_errors.append('Email does not exist.')

    client_otp = user.otp_code if user else ''

    if client_otp != otp_code:
        otp_errors.append('Invalid Code.')

    if email_errors or otp_errors:
        errors['email'] = email_errors
        errors['otp_code'] = otp_errors
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)

    data['email'] = user.email if user else ''
    data['user_id'] = user.user_id if user else ''

    payload['message'] = "Successful"
    payload['data'] = data
    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([AllowAny])
@authentication_classes([])
def resend_password_otp(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []

    email = request.data.get('email', '').lower()

    if not email:
        email_errors.append('Email is required.')
    if email_errors:
        errors['email'] = email_errors
        payload['message'] = "Error"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exist.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    otp_code = generate_random_otp_code()
    user.otp_code = otp_code
    user.save()

    context = {
        'otp_code': otp_code,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    txt_ = get_template("registration/emails/send_otp.txt").render(context)
    html_ = get_template("registration/emails/send_otp.html").render(context)

    subject = 'OTP CODE'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # # Use Celery chain to execute tasks in sequence
    # email_chain = chain(
    #     send_generic_email.si(subject, txt_, from_email, recipient_list, html_),
    #  )
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

    #data["otp_code"] = otp_code
    data["emai"] = user.email
    data["user_id"] = user.user_id

    new_activity = AllActivity.objects.create(
        user=user,
        subject="Password OTP sent",
        body="Password OTP sent to " + user.email,
    )
    new_activity.save()

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([AllowAny])
@authentication_classes([])
def new_password_reset_view(request):
    payload = {}
    data = {}
    errors = {}
    email_errors = []
    password_errors = []

    email = request.data.get('email', '0').lower()
    new_password = request.data.get('new_password')
    new_password2 = request.data.get('new_password2')

    if not email:
        email_errors.append('Email is required.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    qs = User.objects.filter(email=email)
    if not qs.exists():
        email_errors.append('Email does not exists.')
        if email_errors:
            errors['email'] = email_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    if not new_password:
        password_errors.append('Password required.')
        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    if new_password != new_password2:
        password_errors.append('Password don\'t match.')
        if password_errors:
            errors['password'] = password_errors
            payload['message'] = "Error"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_404_NOT_FOUND)

    user = User.objects.filter(email=email).first()
    user.set_password(new_password)
    user.save()

    data['email'] = user.email
    data['user_id'] = user.user_id

    payload['message'] = "Successful, Password reset successfully."
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)


def check_email_exist(email):
    qs = User.objects.filter(email=email)
    if qs.exists():
        return True
    else:
        return False


def check_secretary(email):
    qs = User.objects.filter(email=email)
    if qs.department == "SECRETARY":
        return True
    else:
        return False


def is_valid_email(email):
    # Regular expression pattern for basic email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Using re.match to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


def is_valid_password(password):
    # Check for at least 8 characters
    if len(password) < 8:
        return False

    # Check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False

    # Check for at least one digit
    if not re.search(r'[0-9]', password):
        return False

    # Check for at least one special character
    if not re.search(r'[-!@#\$%^&*_()-+=/.,<>?"~`£{}|:;]', password):
        return False

    return True



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def list_all_users_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    filter_department = request.query_params.get('filter_department', "")
    page_size = 10

    users = User.objects.filter(is_archived=False)

    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(dob__icontains=search_query) |
            Q(marital_status__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(language__icontains=search_query) |
            Q(location_name__icontains=search_query)
        )

    if filter_department:
        users = users.filter(
            Q(department__icontains=filter_department),
        )

    paginator = Paginator(users, page_size)

    try:
        paginated_users = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    users_serializer = ListAllUsersSerializer(paginated_users, many=True)

    data['users'] = users_serializer.data
    data['pagination'] = {
        'page_number': paginated_users.number,
        'total_pages': paginator.num_pages,
        'next': paginated_users.next_page_number() if paginated_users.has_next() else None,
        'previous': paginated_users.previous_page_number() if paginated_users.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def list_all_archived_users_view(request):
    payload = {}
    data = {}
    errors = {}

    search_query = request.query_params.get('search', '')
    page_number = request.query_params.get('page', 1)
    filter_department = request.query_params.get('filter_department', "")
    page_size = 10

    users = User.objects.filter(is_archived=True)

    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(department__icontains=search_query) |
            Q(gender__icontains=search_query) |
            Q(dob__icontains=search_query) |
            Q(marital_status__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(language__icontains=search_query) |
            Q(location_name__icontains=search_query)
        )

    if filter_department:
        users = users.filter(
            Q(department__icontains=filter_department),
        )

    paginator = Paginator(users, page_size)

    try:
        paginated_users = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_users = paginator.page(1)
    except EmptyPage:
        paginated_users = paginator.page(paginator.num_pages)

    users_serializer = ListAllUsersSerializer(paginated_users, many=True)

    data['users'] = users_serializer.data
    data['pagination'] = {
        'page_number': paginated_users.number,
        'total_pages': paginator.num_pages,
        'next': paginated_users.next_page_number() if paginated_users.has_next() else None,
        'previous': paginated_users.previous_page_number() if paginated_users.has_previous() else None,
    }

    payload['message'] = "Successful"
    payload['data'] = data

    return Response(payload, status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def get_user_details_view(request):
    payload = {}
    data = {}
    errors = {}

    user_id = request.query_params.get('user_id', None)

    if not user_id:
        errors['user_id'] = ["User id required"]

    try:
        user = User.objects.get(user_id=user_id)
    except:
        errors['user_id'] = ['User does not exist.']

    if errors:
        payload['message'] = "Errors"
        payload['errors'] = errors
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)




    if user.department == "SECRETARY":
        try:
            secretary = Secretary.objects.get(user=user)
        except:
            errors['secretary_id'] = ['Secretary does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        secretary_serializer = SecretaryDetailsSerializer(secretary, many=False)
        if secretary_serializer:
            user = secretary_serializer.data

    elif user.department == "HUMAN RESOURCES":
        try:
            hr = HumanResource.objects.get(user=user)
        except:
            errors['hr_id'] = ['Human Resource does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        hr_serializer = HumanResourceDetailsSerializer(hr, many=False)
        if hr_serializer:
            user = hr_serializer.data

    elif user.department == "ADMIN":
        try:
            admin = AdminDepartment.objects.get(user=user)
        except:
            errors['admin_id'] = ['Admin does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        admin_serializer = AdminDepartmentDetailsSerializer(admin, many=False)
        if admin_serializer:
            user = admin_serializer.data

    elif user.department == "BILLING":
        try:
            billing = Billing.objects.get(user=user)
        except:
            errors['billing_id'] = ['Billing does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        billing_serializer = BillingDetailsSerializer(billing, many=False)
        if billing_serializer:
            user = billing_serializer.data

    elif user.department == "OPERATIONS":
        try:
            operations = Operation.objects.get(user=user)
        except:
            errors['operation_id'] = ['Operation does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        operations_serializer = OperationsDetailsSerializer(operations, many=False)
        if operations_serializer:
            user = operations_serializer.data

    elif user.department == "COMMERCIAL":
        try:
            commercial = Commercial.objects.get(user=user)
        except:
            errors['commercial_id'] = ['Commercial does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        commercial_serializer = CommercialDetailsSerializer(commercial, many=False)
        if commercial_serializer:
            user = commercial_serializer.data

    elif user.department == "GUARD":
        try:
            guard = SecurityGuard.objects.get(user=user)
        except:
            errors['guard_id'] = ['Guard does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        guard_serializer = SecurityGuardDetailsSerializer(guard, many=False)
        if guard_serializer:
            user = guard_serializer.data

    payload['message'] = "Successful"
    payload['data'] = user

    return Response(payload, status=status.HTTP_200_OK)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = True
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account Archived",
            body=user.email + " account archived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def archive_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = True
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account Archived",
            body=user.email + " account archived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)




@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def unarchive_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']

        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']


        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.is_archived = False
        user.save()

        new_activity = AllActivity.objects.create(
            user=user,
            subject="Account unarchived",
            body=user.email + " account unarchived."
        )
        new_activity.save()

        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)


@api_view(['POST', ])
@permission_classes([IsAuthenticated, ])
@authentication_classes([CustomJWTAuthentication, ])
def delete_user_view(request):
    payload = {}
    data = {}
    errors = {}

    if request.method == 'POST':
        user_id = request.data.get('user_id', "")

        if not user_id:
            errors['user_id'] = ['User ID is required.']


        try:
            user = User.objects.get(user_id=user_id)
        except:
            errors['user_id'] = ['User does not exist.']

        if errors:
            payload['message'] = "Errors"
            payload['errors'] = errors
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)

        user.delete()


        payload['message'] = "Successful"
        payload['data'] = data

    return Response(payload)

