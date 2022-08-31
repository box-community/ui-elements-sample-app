import json

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from apps.authentication.box_jwt import jwt_downscoped_access_token_get
from apps.authentication.util import is_testing
from apps.booking import blueprint
from apps.booking.booking import form_to_booking
from apps.booking.data_seed import data_seed
from apps.booking.demo_folders import booking_diver_folder_get
from apps.booking.forms import BookingForm
from apps.booking.models import Booking, Booking_Diver
from apps.booking.template_helpers import (booking_diver_upload_process, bookings_get_by_user,
                                           get_all_dive_sites_options)
from apps.booking.utils import get_date_tomorrow

@blueprint.route("/bookings", methods=["GET", "POST"])
@login_required
def page_bookings(): # list user bookings
    bookings = bookings_get_by_user(current_user.id)
    return render_template("booking/bookings.html", bookings=bookings)




@blueprint.route("/booking/new", methods=["GET", "POST"])
def page_booking_new():
    data_seed()

    booking_form = BookingForm(request.form)
    booking_form.date.default = get_date_tomorrow()
    booking_form.site.choices = get_all_dive_sites_options()

    if request.method == "POST" or is_testing():
        if booking_form.validate():
            booking_new = form_to_booking(booking_form,current_user.id)

            url = url_for(
                "booking_blueprint.page_booking_upload", booking_id=booking_new.id
            )
            return redirect(url)

    return render_template("booking/booking.html", form=booking_form)


@blueprint.route("/booking/upload", methods=["GET", "POST"])
def page_booking_upload():
    booking_id = request.args.get("booking_id")
    booking = Booking.query.filter_by(id=booking_id).first_or_404()

    booking_diver = Booking_Diver.query.filter_by(booking_id=booking.id).first()

    folder_id_cert = booking_diver_folder_get(booking_diver.id)
    token = jwt_downscoped_access_token_get()
    options = {
        "container": ".uie-upload-cert",
        "fileLimit": 1,
        'modal': None,
    }
    documentType = 'CERTIFICATE'

    return render_template(
        "booking/step2.html",
        form=None,
        token=token,
        folder_id=folder_id_cert,
        options=options,
        documentType=documentType,
        booking_diver_id = booking_diver.id,
    )

@blueprint.route('/event/upload/', methods=['POST'])
def event():
    request_data = request.get_json()
    if not booking_diver_upload_process(request_data):
        return json.dumps({'success':False,'message':'Invalid request'}), 400, {'ContentType':'application/json'} 
        
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    
    

@blueprint.route("/test", methods=["GET", "POST"])
def page_test():
    print(f"***********************  Method: {request.method}")
    return render_template("home/form_elements.html")


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
