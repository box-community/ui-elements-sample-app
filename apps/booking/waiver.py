from pydoc import cli
from apps.authentication.box_jwt import jwt_check_client
from apps.booking.models import Booking, Booking_Diver, Diver
from apps import Config

from boxsdk import BoxAPIException

def booking_diver_waiver_sign(booking_diver_id: int) -> dict:
    """Sign a waiver for a booking diver"""
    
    template_id   = Config.SIGN_TEMPLATE_ID
    
    booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()
    diver = Diver.query.filter_by(id=booking_diver.diver_id).first()

    client = jwt_check_client()

    file = client.file(template_id).get()

    file_to_sign = {
        'id': file.id,
        'type': 'file',
    }

    signer = {
        'name': diver.name,
        'email': diver.email,

    }


    sign_request = client.create_sign_request(
        files = [file_to_sign],
        signers = [signer],
        parent_folder_id = booking_diver.folder_id,
        external_id = str(booking_diver.id),
        email_subject = 'Box Dive Waiver Sign Request for '+diver.name,
        email_message = 'Please sign this document by clicking the review document button above.<br><br>Kind regards,<br><br>Box Dive',
        )

    return sign_request