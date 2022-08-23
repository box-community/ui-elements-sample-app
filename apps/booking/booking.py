from datetime import date
from apps import db
from apps.booking.forms import BookingForm
from apps.booking.models import Booking, Booking_Diver, Diver


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


def booking_diver_create(booking_id: int, diver_id: int):
    """Create a new booking diver"""
    booking_diver = Booking_Diver(booking_id=booking_id, diver_id=diver_id)
    db.session.add(booking_diver)
    db.session.commit()
    return booking_diver


def booking_diver_get_by_booking_and_diver(booking_id: int, diver_id: int):
    """Get booking diver by booking and diver"""
    return Booking_Diver.query.filter_by(
        booking_id=booking_id, diver_id=diver_id
    ).first()


def booking_diver_get_or_create(booking_id: int, diver_id: int):
    """Get booking diver by booking and diver or create a new booking diver"""
    booking_diver = booking_diver_get_by_booking_and_diver(booking_id, diver_id)
    if not booking_diver:
        booking_diver = booking_diver_create(booking_id=booking_id, diver_id=diver_id)
    return booking_diver


def booking_from_data(site_id: int, date: date, name: str, email: str):
    """Create a new booking from data"""
    booking = booking_get_or_create(site_id, date)
    diver = diver_get_or_create(name, email)
    booking_diver = booking_diver_get_or_create(booking.id, diver.id)
    return booking


def form_to_booking(booking_form: BookingForm):
    """Create a new booking from form"""
    booking = booking_from_data(
        booking_form.site.data,
        booking_form.date.data,
        booking_form.name.data,
        booking_form.email.data,
    )

    return booking
