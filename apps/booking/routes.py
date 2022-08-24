from apps.authentication.box_jwt import (
    jwt_check_client,
    jwt_downscoped_access_token_get,
)
from apps.booking import blueprint
from apps.booking.booking import form_to_booking
from apps.booking.data_seed import data_seed
from apps.booking.forms import BookingForm
from apps.booking.template_helpers import get_all_dive_sites_options
from apps.booking.utils import get_date_tomorrow
from flask import render_template, request, redirect, url_for
from apps.authentication.util import is_testing
from apps.booking.models import Booking, Booking_Diver, Diver
from apps.booking.demo_folders import booking_diver_folder_get


@blueprint.route("/booking", methods=["GET", "POST"])
def page_booking():
    data_seed()

    booking = BookingForm(request.form)
    booking.date.default = get_date_tomorrow()
    booking.site.choices = get_all_dive_sites_options()

    if request.method == "POST" or is_testing():
        if booking.validate():
            booking_new = form_to_booking(booking)

            url = url_for(
                "booking_blueprint.page_booking_upload", booking_id=booking_new.id
            )
            return redirect(url)

    return render_template("booking/booking.html", form=booking)


@blueprint.route("/booking/upload", methods=["GET", "POST"])
def page_booking_upload():
    booking_id = request.args.get("booking_id")
    booking = Booking.query.filter_by(id=booking_id).first()
    booking_diver = Booking_Diver.query.filter_by(booking_id=booking_id).first()

    folder_id_cert = booking_diver_folder_get(booking_diver.id)
    token = jwt_downscoped_access_token_get()
    options = {
        "container": ".uie-upload-cert",
        "fileLimit": 1,
        'modal': None,
    }

    return render_template(
        "booking/step2.html",
        form=None,
        token=token,
        folder_id=folder_id_cert,
        options=options,
    )


@blueprint.route("/test", methods=["GET", "POST"])
def page_test():
    print(f"***********************  Method: {request.method}")
    return render_template("home/form_elements.html")
