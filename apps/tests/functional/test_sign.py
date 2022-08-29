from datetime import date, timedelta
import json
import os
from apps.authentication.box_jwt import jwt_check_client
from apps.booking.demo_folders import booking_diver_folder_get, booking_folder_get
from apps.booking.models import Booking, Booking_Diver, Diver
from apps.booking.booking import booking_from_data
from apps.booking.waiver import booking_diver_waiver_sign
from boxsdk import BoxAPIException

def test_sign(test_client, init_database, new_diver_barbas):
    """
    GIVEN a booking diver id
    WHEN a waiver sign is requested
    THEN a sign request is created
    """

    book_date = date.today() + timedelta(days=3)
    booking = booking_from_data(1, book_date, new_diver_barbas.name, new_diver_barbas.email)
    booking_diver = Booking_Diver.query.filter_by(booking_id=booking.id).first()
    diver = Diver.query.filter_by(email=new_diver_barbas.email).first()
    bd_id = booking_diver.id

    assert booking is not None

    booking_folder_id = booking_folder_get(booking.id)

    assert booking_folder_id is not None

    booking_diver_folder_id = booking_diver_folder_get(booking_diver.id)

    assert booking_diver_folder_id is not None

    # Create a waiver sign request
    client = jwt_check_client()
    
    sign_request = booking_diver_waiver_sign(bd_id)

    sign_request_check = client.sign_request(sign_request_id = sign_request.id)
    
    assert sign_request == sign_request_check

    sign_requests = client.get_sign_requests()
    try:
        for item in sign_requests:
            print(f"{item.id} {item.status} {item.expires_at} {item.created_at} {item.signed_at} {item.external_id}")
    except BoxAPIException as e:
        print(e)
    except Exception as e:
        print(e)



    