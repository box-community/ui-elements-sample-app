from datetime import date, timedelta
from apps.booking.models import Booking, Booking_Diver, Diver
from apps.booking.booking import booking_from_data


def test_booking_upload(test_client,init_database,new_diver_john ,new_diver_jane):
    """
    GIVEN an upload page
    WHEN redered
    THEN show booking details
    """

    book_date = date.today() + timedelta(days=5)
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
    assert b"Upload Certification" in response.data
