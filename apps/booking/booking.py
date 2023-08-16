""" bookings"""
from datetime import date, timedelta, datetime
from apps import db
from apps.authentication.box_jwt import jwt_check_client
from apps.booking.forms import BookingForm
from apps.booking.models import Booking, Booking_Diver, Diver
from apps.booking.demo_folders import booking_diver_folder_create
from apps import Config


def booking_create(dive_site_id: int, date: date):
    """Create a new booking"""
    booking = Booking(date=date, dive_site_id=dive_site_id)
    db.session.add(booking)
    db.session.commit()
    return booking


def booking_get_by_site_and_date(dive_site_id: int, date: date):
    """Get booking by dive site and date"""
    return Booking.query.filter_by(dive_site_id=dive_site_id, date=date).first()


def booking_get_or_create(dive_site_id: int, date: date):
    """Get booking by dive site and date or create a new booking"""
    booking = booking_get_by_site_and_date(dive_site_id=dive_site_id, date=date)
    if not booking:
        booking = booking_create(dive_site_id=dive_site_id, date=date)
    return booking


def diver_get_by_email(email: str):
    """Get diver by email"""
    return Diver.query.filter_by(email=email).first()


def diver_create(name: str, email: str):
    """Create a new diver"""
    diver = Diver(name=name, email=email)
    db.session.add(diver)
    db.session.commit()
    return diver


def diver_get_or_create(name: str, email: str):
    """Get diver by email or create a new diver"""
    diver = diver_get_by_email(email=email)
    if not diver:
        diver = diver_create(name=name, email=email)
    return diver


def booking_diver_create(booking_id: int, diver_id: int, created_by: int):
    """Create a new booking diver"""
    booking_diver = Booking_Diver(booking_id=booking_id, diver_id=diver_id, created_by=created_by)
    db.session.add(booking_diver)
    db.session.commit()
    booking_diver_folder_create(booking_diver.id)
    return booking_diver


def booking_diver_get_by_booking_and_diver(booking_id: int, diver_id: int):
    """Get booking diver by booking and diver"""
    return Booking_Diver.query.filter_by(booking_id=booking_id, diver_id=diver_id).first()


def booking_diver_get_or_create(booking_id: int, diver_id: int, created_by: int):
    """Get booking diver by booking and diver or create a new booking diver"""
    booking_diver = booking_diver_get_by_booking_and_diver(booking_id, diver_id)
    if not booking_diver:
        booking_diver = booking_diver_create(booking_id=booking_id, diver_id=diver_id, created_by=created_by)
    return booking_diver


def booking_from_data(site_id: int, date: date, name: str, email: str, created_by: int):
    """Create a new booking from data"""
    booking = booking_get_or_create(site_id, date)
    diver = diver_get_or_create(name, email)
    booking_diver = booking_diver_get_or_create(booking.id, diver.id, created_by)
    return booking


def form_to_booking(booking_form: BookingForm, created_by: str):
    """Create a new booking from form"""
    booking = booking_from_data(
        booking_form.site.data, booking_form.date.data, booking_form.name.data, booking_form.email.data, created_by
    )

    return booking


def booking_diver_trigger_task_certification(booking_diver_id: int):
    """Trigger task for booking diver"""
    booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()
    booking = Booking.query.filter_by(id=booking_diver.booking_id).first()

    client = jwt_check_client()
    tasks = client.file(booking_diver.certification_file_id).get_tasks()

    for task_item in tasks:
        for entry in task_item["task_assignment_collection"]["entries"]:
            if entry is not None:
                task = task_item

    due_date = booking.date

    if due_date <= datetime.now().date():
        due_date = datetime.now() + timedelta(days=1)

    due_date = datetime.combine(due_date, datetime.min.time())

    users = client.users(user_type="managed")
    sign_admin = None
    for user in users:
        # print(f"{user.name} (User ID: {user.id})")
        if user.login == Config.TASK_USER_ID:
            sign_admin = user
            break

    task = None
    if task is None:
        task = client.file(booking_diver.certification_file_id).create_task(
            action="review", completion_rule="any_assignee", due_at=due_date, message="Verify certification"
        )

    # TODO: If the task assignment already exists then do not duplicate the assignment
    assignment = client.task(task_id=task.id).assign(sign_admin)

    booking_diver.certification_task_id = assignment.id
    booking_diver.certification_status = assignment.status

    db.session.commit()

    return task


def booking_diver_trigger_task_insurance(booking_diver_id: int):
    """Trigger task for booking diver"""
    booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()
    booking = Booking.query.filter_by(id=booking_diver.booking_id).first()

    client = jwt_check_client()
    tasks = client.file(booking_diver.insurance_file_id).get_tasks()

    for task_item in tasks:
        for entry in task_item["task_assignment_collection"]["entries"]:
            if entry is not None:
                task = task_item

    due_date = booking.date

    if due_date <= datetime.now().date():
        due_date = datetime.now() + timedelta(days=1)

    due_date = datetime.combine(due_date, datetime.min.time())

    users = client.users(user_type="managed")
    sign_admin = None

    for user in users:
        # print(f"{user.name} (User ID: {user.id})")
        if user.login == Config.TASK_USER_ID:
            sign_admin = user
            break

    task = None
    if task is None:
        task = client.file(booking_diver.insurance_file_id).create_task(
            action="review", completion_rule="any_assignee", due_at=due_date, message="Verify insurance"
        )

    # TODO: If the task assignment already exists then do not duplicate the assignment
    assignment = client.task(task_id=task.id).assign(sign_admin)

    booking_diver.insurance_task_id = assignment.id
    booking_diver.insurance_status = assignment.status

    db.session.commit()

    return task


def booking_diver_trigger_task_waiver(booking_diver_id: int):
    """Trigger task for booking diver"""
    booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()
    booking = Booking.query.filter_by(id=booking_diver.booking_id).first()

    client = jwt_check_client()
    tasks = client.file(booking_diver.waiver_file_id).get_tasks()

    task = None
    for task_item in tasks:
        for entry in task_item["task_assignment_collection"]["entries"]:
            if entry is not None:
                task = task_item

    due_date = booking.date

    if due_date <= datetime.now().date():
        due_date = datetime.now() + timedelta(days=1)

    due_date = datetime.combine(due_date, datetime.min.time())

    users = client.users(user_type="managed")
    sign_admin = None
    for user in users:
        # print(f"{user.name} (User ID: {user.id})")
        if user.login == Config.TASK_USER_ID:
            sign_admin = user
            break

    if task is None:
        task = client.file(booking_diver.waiver_file_id).create_task(
            action="review", completion_rule="any_assignee", due_at=due_date, message="Verify waiver"
        )

    # TODO: If the task assignment already exists then do not duplicate the assignment
    assignment = client.task(task_id=task.id).assign(sign_admin)

    booking_diver.waiver_task_id = assignment.id
    booking_diver.waiver_status = assignment.status

    db.session.commit()

    return task
