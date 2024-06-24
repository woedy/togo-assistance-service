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

def unique_complaint_id_generator(instance):
    """
    This is for a complaint_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    complaint_id = "COMP-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(C)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(complaint_id=complaint_id).exists()
    if qs_exists:
        return None
    return complaint_id

def unique_supplier_id_generator(instance):
    """
    This is for a supplier_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    supplier_id = "SUP-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(LIR)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(supplier_id=supplier_id).exists()
    if qs_exists:
        return None
    return supplier_id


def unique_site_id_generator(instance):
    """
    This is for a site_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    site_id = "SYT-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(E)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(site_id=site_id).exists()
    if qs_exists:
        return None
    return site_id

def unique_zone_id_generator(instance):
    """
    This is for a zone_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    zone_id = "ZN-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(Z)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(zone_id=zone_id).exists()
    if qs_exists:
        return None
    return zone_id

def unique_estimate_id_generator(instance):
    """
    This is for a estimate_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    estimate_id = "EST-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(P)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(estimate_id=estimate_id).exists()
    if qs_exists:
        return None
    return estimate_id

def unique_contract_id_generator(instance):
    """
    This is for a contract_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    contract_id = "CON-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(T)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(contract_id=contract_id).exists()
    if qs_exists:
        return None
    return contract_id


def unique_legal_id_generator(instance):
    """
    This is for a legal_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    legal_id = "LG-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(J)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(legal_id=legal_id).exists()
    if qs_exists:
        return None
    return legal_id



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




def unique_payment_id_generator(instance):
    """
    This is for a payment_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    payment_id = "PAY-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(NT)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(payment_id=payment_id).exists()
    if qs_exists:
        return None
    return payment_id




def unique_log_id_generator(instance):
    """
    This is for a log_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    log_id = "LOG-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(C)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(log_id=log_id).exists()
    if qs_exists:
        return None
    return log_id





def unique_category_id_generator(instance):
    """
    This is for a category_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    category_id = "CAT-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(RY)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(category_id=category_id).exists()
    if qs_exists:
        return None
    return category_id


def unique_payroll_id_generator(instance):
    """
    This is for a payroll_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    payroll_id = "PAYROLL-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(PR)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(payroll_id=payroll_id).exists()
    if qs_exists:
        return None
    return payroll_id



def unique_equipment_id_generator(instance):
    """
    This is for a equipment_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    equipment_id = "EQ-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(NT)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(equipment_id=equipment_id).exists()
    if qs_exists:
        return None
    return equipment_id



def unique_inventory_id_generator(instance):
    """
    This is for a inventory_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    inventory_id = "INV-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(RY)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(inventory_id=inventory_id).exists()
    if qs_exists:
        return None
    return inventory_id


def unique_assignment_id_generator(instance):
    """
    This is for a assignment_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    assignment_id = "ASS-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(NT)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(assignment_id=assignment_id).exists()
    if qs_exists:
        return None
    return assignment_id



def unique_order_id_generator(instance):
    """
    This is for a order_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    order_id = "ORD-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(ER)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        return None
    return order_id



def unique_order_item_id_generator(instance):
    """
    This is for a order_item_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    order_item_id = "ORD/IT-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(IT)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_item_id=order_item_id).exists()
    if qs_exists:
        return None
    return order_item_id




def unique_maintenance_id_generator(instance):
    """
    This is for a maintenance_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    maintenance_id = "MAINT-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(NCE)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(maintenance_id=maintenance_id).exists()
    if qs_exists:
        return None
    return maintenance_id

def unique_deployment_id_generator(instance):
    """
    This is for a deployment_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    deployment_id = "DEP-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-(LOY)"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(deployment_id=deployment_id).exists()
    if qs_exists:
        return None
    return deployment_id

def unique_attendance_id_generator(instance):
    """
    This is for a attendance_id field
    :param instance:
    :return:
    """
    size = random.randint(5, 7)
    attendance_id = "att-" + random_string_generator(size=size, chars=string.ascii_uppercase + string.digits) + "-ce"

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(attendance_id=attendance_id).exists()
    if qs_exists:
        return None
    return attendance_id
