"""
Functional tests for the `booking` blueprint.

These tests use GETs and POSTs to different URLs to check for the proper behavior
of the blueprint.
"""


from datetime import date, datetime, timedelta
import email
from apps.booking.models import Booking, Booking_Diver, Diver

url_home = "/home"

def test_booking_start(test_client, init_database,login_user):
    """
    GIVEN a Flask application configured for testing
    WHEN the home page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get(url_home)
    assert response.status_code == 200
    assert b"Dive Into the Box" in response.data
    assert b"Booking Date" in response.data
    assert b"Test dive site 1" in response.data


def test_booking_submit(test_client, init_database,login_user):
    """
    GIVEN the new booking page
    WHEN the user enters date, site, name and email
    THEN a bookinfg should be created
    """

    book_date = date.today() + timedelta(days=5)

    response = test_client.post(
        url_home,
        data=dict(date=book_date, site=1),
        follow_redirects=False,
    )

    assert response.status_code == 200 or response.status_code == 302

    # was booking created?
    booking = Booking.query.filter_by(date=book_date, dive_site_id=1).first()
    assert booking is not None
    assert booking.date == book_date
    assert booking.dive_site_id == 1

    #TODO: create test for diver
    # # diver exists?
    # diver = Diver.query.filter_by(name="John Smith", email="sjohn@example.com").first()
    # assert diver is not None
    # assert diver.name == "John Smith"
    # assert diver.email == "sjohn@example.com"

    # # booking diver exists?
    # booking_diver = Booking_Diver.query.filter_by(
    #     booking_id=booking.id, diver_id=diver.id
    # ).first()

    # assert booking_diver is not None
    # assert booking_diver.booking_id == booking.id
    # assert booking_diver.diver_id == diver.id

def test_booking_submit_duplicate(test_client, init_database, new_diver_john,login_user):
    """
    GIVEN the new booking page
    WHEN the user enters date, site, name and email
    AND then date, site, name and email are duplicated
    THEN a bookinfg should be created but not duplicated
    
    """

    book_date = date.today() + timedelta(days=5)

    response = test_client.post(
        url_home,
        data=dict(date=book_date, site=1),
        follow_redirects=False,
    )

    assert response.status_code == 200 or response.status_code == 302

    # was booking created?
    booking = Booking.query.filter_by(date=book_date, dive_site_id=1).first()
    assert booking is not None
    assert booking.date == book_date
    assert booking.dive_site_id == 1

    # Duplicate the booking
    response = test_client.post(
        url_home,
        data=dict(date=book_date, site=1),
        follow_redirects=False,
    )

    assert response.status_code == 200 or response.status_code == 302
    # was booking created?
    booking_dup = Booking.query.filter_by(date=book_date, dive_site_id=1).first()
    assert booking_dup is not None
    assert booking_dup.date == book_date
    assert booking_dup.dive_site_id == 1
    assert booking_dup.id == booking.id


    # # diver exists (db constraints do not allow duplicate emails)?
    # diver = Diver.query.filter_by(email=new_diver_john.email).first()
    # assert diver is not None
    # assert diver.name == new_diver_john.name
    # assert diver.email == new_diver_john.email

    # # booking diver exists?
    # booking_divers = Booking_Diver.query.filter_by(booking_id=booking.id, diver_id=diver.id).all()

    # assert booking_divers is not None
    # assert len(booking_divers) == 1
    
def test_booking_submit_new_diver(test_client, init_database,new_diver_john ,new_diver_jane,login_user):
    """
    GIVEN the new booking page
    WHEN the user enters date, site, name and email
    AND then date, site, are duplicated
    THEN a bookinfg should exist with the new diver assigned to it
    
    """

    book_date = date.today() + timedelta(days=5)


    # create booking
    response = test_client.post(
        url_home,
        data=dict(date=book_date, site=1),
        follow_redirects=False,
    )

    assert response.status_code == 200 or response.status_code == 302

    # was booking created?
    booking = Booking.query.filter_by(date=book_date, dive_site_id=1).first()
    assert booking is not None
    assert booking.date == book_date
    assert booking.dive_site_id == 1

    url_new_diver = "/booking/"+str(booking.id)+"/newdiver"

     # book for Jane
    response = test_client.post(
        url_new_diver,
        data=dict(name=new_diver_jane.name, email=new_diver_jane.email),
        follow_redirects=False,
    )

    assert response.status_code == 200 or response.status_code == 302

    # diver exists?
    diver_jane = Diver.query.filter_by(name=new_diver_jane.name, email=new_diver_jane.email).first()
    assert diver_jane is not None

    response = test_client.post(
        url_new_diver,
        data=dict(name=new_diver_john.name, email=new_diver_john.email),
        follow_redirects=False,
    )

    assert response.status_code == 200 or response.status_code == 302

    # diver exists?
    diver_john = Diver.query.filter_by(name=new_diver_john.name, email=new_diver_john.email).first()







    