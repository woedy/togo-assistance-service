import random
import re
import string
from django.contrib.auth import get_user_model, authenticate




def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def generate_random_otp_code():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code


def unique_user_id_generator(instance):
    """
    This is for a django project with a user_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    user_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=user_id).exists()
    if qs_exists:
        return
    return user_id






def generate_email_token():
    code = ''
    for i in range(4):
        code += str(random.randint(0, 9))
    return code




def unique_user_id_generator(instance):
    """
    This is for a django project with a user_id field
    :param instance:
    :return:
    """

    size = random.randint(30,45)
    user_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(user_id=user_id).exists()
    if qs_exists:
        return
    return user_id



def unique_guard_id_generator(instance):
    """
    This is for a guard_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    guard_id = "GD-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(S)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(guard_id=guard_id).exists()
    if qs_exists:
        return None
    return guard_id

def unique_secretary_id_generator(instance):
    """
    This is for a secretary_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    secretary_id = "SE-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(A)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(secretary_id=secretary_id).exists()
    if qs_exists:
        return None
    return secretary_id

def unique_hr_id_generator(instance):
    """
    This is for a hr_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    hr_id = "HR-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(A)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(hr_id=hr_id).exists()
    if qs_exists:
        return None
    return hr_id

def unique_admin_id_generator(instance):
    """
    This is for a admin_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    admin_id = "AD-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(A)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(admin_id=admin_id).exists()
    if qs_exists:
        return None
    return admin_id


def unique_operations_id_generator(instance):
    """
    This is for a operations_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    operations_id = "OP-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(T)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(operations_id=operations_id).exists()
    if qs_exists:
        return None
    return operations_id

def unique_billing_id_generator(instance):
    """
    This is for a billing_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    billing_id = "BI-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(T)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(billing_id=billing_id).exists()
    if qs_exists:
        return None
    return billing_id

def unique_commercial_id_generator(instance):
    """
    This is for a commercial_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    commercial_id = "CO-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(C)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(commercial_id=commercial_id).exists()
    if qs_exists:
        return None
    return commercial_id


def unique_client_id_generator(instance):
    """
    This is for a guard_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    client_id = "CL-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(C)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(client_id=client_id).exists()
    if qs_exists:
        return None
    return client_id
def unique_operations_id_generator(instance):
    """
    This is for a operations_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    operations_id = "OP-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(C)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(operations_id=operations_id).exists()
    if qs_exists:
        return None
    return operations_id


def unique_room_id_generator(instance):
    """
    This is for a room_id field
    :param instance:
    :return:
    """
    size = random.randint(30, 45)
    room_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(room_id=room_id).exists()
    if qs_exists:
        return None
    return room_id



def unique_booking_id_generator(instance):
    """
    This is for a booking_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    booking_id = "BUK-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(AP)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(booking_id=booking_id).exists()
    if qs_exists:
        return None
    return booking_id
