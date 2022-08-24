from datetime import date, timedelta
from apps.authentication.box_jwt import jwt_check_client
from apps.booking.demo_folders import booking_diver_folder_get, booking_folder_get
from apps.booking.models import Booking, Booking_Diver, Diver
from apps.booking.booking import booking_from_data
from boxsdk import BoxAPIException

def test_booking_folder_get(test_client,init_database,new_diver_john ,new_diver_jane):
    """
    GIVEN a booking
    WHEN the app needs to upload a file to the diver folder
    THEN system must have created the folder structure
    AND return the folder for this specific diver booking
    """

    book_date = date.today() + timedelta(days=1)
    booking = booking_from_data(1,book_date,new_diver_john.name,new_diver_john.email)
    booking_diver = Booking_Diver.query.filter_by(booking_id=booking.id).first()

    assert booking is not None

    booking_folder_id = booking_folder_get(booking.id)

    assert booking_folder_id is not None

    booking_diver_folder_id = booking_diver_folder_get(booking_diver.id)

    assert booking_diver_folder_id is not None



    # TODO: check what happens if the folder is accidentally deleted

    # delete the folder
    client = jwt_check_client()

    client.folder(booking_diver_folder_id).delete()

    booking_diver_folder_id = booking_diver_folder_get(booking_diver.id)

    try:
        folder = client.folder(booking_diver_folder_id+'1').get()

    except BoxAPIException as e:
        assert e.status == 404
        assert False
    
    assert folder is not None

    



def test_booking_upload(test_client,init_database,new_diver_john ,new_diver_jane):
    """
    GIVEN an upload page
    WHEN redered
    THEN show booking details
    """

    book_date = date.today() + timedelta(days=2)
    booking_from_data(1,book_date,new_diver_jane.name,new_diver_jane.email)
    booking = booking_from_data(1,book_date,new_diver_john.name,new_diver_john.email)

    assert booking is not None


    booking = Booking.query.order_by(Booking.id.desc()).first()
    response = test_client.get(
        "/booking/upload",
        query_string={"booking_id": booking.id},
        follow_redirects=False,
    )

    assert response.status_code == 200
    assert b"Upload Documents" in response.data
    
    assert b"Booking Details" in response.data


    assert b"Upload Dive Certification Card" in response.data

