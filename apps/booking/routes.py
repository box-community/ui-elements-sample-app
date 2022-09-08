import json

from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from apps.authentication.box_jwt import jwt_downscoped_access_token_get
from apps.authentication.util import is_testing
from apps.booking import blueprint
from apps.booking.booking import booking_create, booking_diver_create, booking_diver_get_or_create, booking_get_or_create, diver_get_or_create, form_to_booking
from apps.booking.data_seed import data_seed
from apps.booking.demo_folders import booking_diver_folder_get
from apps.booking.forms import BookingSimpleForm, BookingForm, DiverForm
from apps.booking.models import Booking, Booking_Diver
from apps.booking.template_helpers import (booking_diver_upload_process, booking_get_by_id, bookings_get_by_user,
                                           get_all_dive_sites_options)
from apps.booking.utils import get_all_dive_sites, get_date_tomorrow
from apps.booking.waiver import booking_diver_waiver_sign

@blueprint.route('/')
@blueprint.route('/home', methods=["GET", "POST"])
@login_required
def page_home():
    """
    Home page of the booking app.
    """
    data_seed()
    
    form_booking_new = BookingSimpleForm(request.form)

    dive_sites = get_all_dive_sites()

    if request.method == "POST" or is_testing():
        if form_booking_new.validate_on_submit():
            booking_date = form_booking_new.date.data
            booking_site = form_booking_new.site.data
            booking = booking_get_or_create(booking_site, booking_date)
            return redirect(url_for('booking_blueprint.page_booking_new_diver', booking_id=booking.id))
    
    return render_template('booking/home.html', avatar_url = current_user.avatar_url, title='Home',segment = 'home', dive_sites = dive_sites, form = form_booking_new)



@blueprint.route("/bookings", methods=["GET", "POST"])
@login_required
def page_bookings(): # list user bookings
    bookings = bookings_get_by_user(current_user.id)
    return render_template("booking/bookings.html", avatar_url = current_user.avatar_url, bookings=bookings,segment='bookings')



@blueprint.route("/booking/<int:booking_id>", methods=["GET", "POST"])
@login_required
def page_booking(booking_id): # Show booking details
    booking = booking_get_by_id(booking_id, current_user.id)
    token = jwt_downscoped_access_token_get()
    
    for booking_diver in booking.booking_divers:
        cert_folder = booking_diver_folder_get(booking_diver.id)


    return render_template("booking/booking.html", avatar_url = current_user.avatar_url, booking=booking, token=token)



@blueprint.route("/booking/<int:booking_id>/newdiver", methods=["GET", "POST"])
@login_required
def page_booking_new_diver(booking_id):
    """ add a new diver to an existing bookikng"""

    booking = booking_get_by_id(booking_id, current_user.id)
    form_diver = DiverForm()

    if request.method == "POST" or is_testing():
        if form_diver.validate_on_submit():
            diver = diver_get_or_create(form_diver.name.data, form_diver.email.data)
            booking_diver = booking_diver_get_or_create(booking.id, diver.id, current_user.id)
            sign_request = booking_diver_waiver_sign(booking_diver.id)
            return redirect(url_for('booking_blueprint.page_booking', booking_id=booking_id))

    return render_template("booking/booking_new_diver.html", avatar_url = current_user.avatar_url, booking=booking, form=form_diver)



@blueprint.route('/event/upload/', methods=['POST'])
def event_upload():
    request_data = request.get_json()
    if not booking_diver_upload_process(request_data):
        return json.dumps({'success':False,'message':'Invalid request'}), 400, {'ContentType':'application/json'} 
        
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    
    

@blueprint.route("/form_elements", methods=["GET", "POST"])
def page_test():
    print(f"***********************  Method: {request.method}")
    return render_template("home/form_elements.html")

@blueprint.route("/old_index", methods=["GET", "POST"])
def page_old_index():
    print(f"***********************  Method: {request.method}")
    return render_template("home/index orig.html")    

@blueprint.route("/tbl_bootstrap", methods=["GET", "POST"])
def page_tbl_bootstrap():
    print(f"***********************  Method: {request.method}")
    return render_template("home/tbl_bootstrap.html")    

@blueprint.route("/icon-feather", methods=["GET", "POST"])
def page_icon_feather():
    print(f"***********************  Method: {request.method}")
    return render_template("home/icon-feather.html")   


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
