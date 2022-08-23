from datetime import datetime
from apps.booking.models import Booking, Dive_Site, Diver, Booking_Diver
from apps import db

def test_new_dive_site(init_db):
    """
    GIVEN a dive_site model
    WHEN a new dive_site is created
    THEN check the name and id are defined correctly
    """

    dive_site = Dive_Site(name = 'Test dive site')
    db.session.add(dive_site)
    db.session.commit()
    assert dive_site is not None
    assert dive_site.name == 'Test dive site'
    assert dive_site.id is not None


def test_new_diver(init_db):
    """
    GIVEN a divers model
    WHEN a new divers is created
    THEN check the if fields are defined correctly
    """
    
    diver = Diver(name = 'John Smith', email = 'johns@gmail.com')
    db.session.add(diver)
    db.session.commit()
    assert diver is not None
    assert diver.name == 'John Smith'
    assert diver.email == 'johns@gmail.com'
    assert diver.id is not None

def test_new_booking(init_db):
    """
    GIVEN a booking model
    WHEN a new booking is created
    THEN check the if fields are defined correctly
    """
    
    current_date = datetime.now().date()
    booking = Booking(date = current_date, dive_site_id = 1, created_by = 1)
    db.session.add(booking)
    db.session.commit()
    assert booking is not None
    assert booking.date == current_date
    assert booking.dive_site_id == 1
    assert booking.id is not None

def test_new_booking_diver(init_db):
    """
    GIVEN a booking_diver model
    WHEN a new booking_diver is created
    THEN check the if fields are defined correctly
    """
    
    booking_diver = Booking_Diver(booking_id = 1, diver_id = 1)
    db.session.add(booking_diver)
    db.session.commit()
    assert booking_diver is not None
    assert booking_diver.booking_id == 1
    assert booking_diver.diver_id == 1
    assert booking_diver.id is not None