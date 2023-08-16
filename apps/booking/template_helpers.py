"""
functions to help with templates
"""
from apps.booking.booking import booking_diver_trigger_task_certification, booking_diver_trigger_task_insurance
from apps.booking.models import Booking, Booking_Diver, Dive_Site, Diver
from apps import db


def get_all_dive_sites():
    """
    Return a list of Dive_Site objects.
    """
    dive_sites = Dive_Site.query.all()
    return dive_sites


def get_all_dive_sites_options():
    """
    Return a list of tuples with the dive site id and name.
    """

    mylist = get_all_dive_sites()

    options = []
    for row in mylist:
        options.append((row.id, row.name))

    options.insert(0, ("", "Select a dive site"))

    return options


def booking_diver_upload_process(data) -> bool:
    """
    Process the upload of a certificate or insurance car for a booking diver.
    """

    if data["eventType"] == "complete":
        if data["documentType"] == "CERTIFICATE":
            if data["e"][0]["type"] == "file":
                if data["e"][0]["id"] is not None:
                    booking_diver = Booking_Diver.query.filter_by(id=data["booking_diver_id"]).first()
                    booking_diver.certification_file_id = data["e"][0]["id"]
                    db.session.commit()
                    booking_diver_trigger_task_certification(booking_diver.id)

                    return True
        elif data["documentType"] == "INSURANCE":
            if data["e"][0]["type"] == "file":
                if data["e"][0]["id"] is not None:
                    booking_diver = Booking_Diver.query.filter_by(id=data["booking_diver_id"]).first()
                    booking_diver.insurance_file_id = data["e"][0]["id"]
                    booking_diver_trigger_task_insurance(booking_diver.id)
                    db.session.commit()
                    return True

    return False


def bookings_get_by_user(user_id: int) -> list:
    """
    Get all bookings for a user.
    """

    bookings = (
        Booking.query.join(Booking_Diver, Booking.id == Booking_Diver.booking_id)
        .filter(Booking_Diver.created_by == user_id)
        .all()
    )

    for booking in bookings:
        booking.booking_divers = Booking_Diver.query.filter_by(booking_id=booking.id, created_by=user_id).all()
        booking.dive_site = Dive_Site.query.filter_by(id=booking.dive_site_id).first()
        for booking_diver in booking.booking_divers:
            booking_diver.diver = Diver.query.filter_by(id=booking_diver.diver_id).first()

    return bookings


def booking_get_by_id(booking_id: int, created_by: int) -> Booking:
    """
    Get a booking by id.
    """

    # booking = Booking.query.join(Booking_Diver, Booking.id == Booking_Diver.booking_id).filter(Booking_Diver.created_by == created_by).filter_by(id=booking_id).first()
    booking = Booking.query.filter_by(id=booking_id).first()
    booking.booking_divers = Booking_Diver.query.filter_by(booking_id=booking.id, created_by=created_by).all()
    booking.dive_site = Dive_Site.query.filter_by(id=booking.dive_site_id).first()
    for booking_diver in booking.booking_divers:
        booking_diver.diver = Diver.query.filter_by(id=booking_diver.diver_id).first()

    return booking
