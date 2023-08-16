from apps.authentication.box_jwt import jwt_check_client
from apps.booking.booking import booking_diver_trigger_task_waiver
from apps.booking.demo_folders import booking_diver_folder_create
from apps.booking.models import Booking_Diver, Diver
from apps import Config, db


def booking_diver_waiver_sign(booking_diver_id: int) -> dict:
    """Sign a waiver for a booking diver"""

    template_id = Config.SIGN_TEMPLATE_ID

    booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()

    if not booking_diver.folder_id:
        folder_id = booking_diver_folder_create(booking_diver_id)
    else:
        folder_id = booking_diver.folder_id

    diver = Diver.query.filter_by(id=booking_diver.diver_id).first()
    bd_id = booking_diver.id

    client = jwt_check_client()

    file = client.file(template_id).get()

    file_to_sign = {
        "id": file.id,
        "type": "file",
    }

    signer = {
        "name": diver.name,
        "email": diver.email,
    }

    sign_request = client.create_sign_request(
        files=[file_to_sign],
        signers=[signer],
        parent_folder_id=folder_id,
        external_id=str(booking_diver.id),
        email_subject="Box Dive Waiver Sign Request for " + diver.name,
        email_message="Please sign this document by clicking the review document button above.<br><br>Kind regards,<br><br>Box Dive",
    )

    booking_diver = Booking_Diver.query.filter_by(id=bd_id).first()
    booking_diver.waiver_file_id = sign_request.sign_files["files"][0].id
    booking_diver_trigger_task_waiver(bd_id)
    db.session.commit()
    return sign_request
