from flask import render_template,request
from apps.booking import blueprint
from apps.booking.forms import BookingForm
from apps.booking.data_seed import data_seed
from apps.booking.template_helpers import get_all_dive_sites_options
from apps.booking.utils import get_date_tomorrow

@blueprint.route('/booking', methods=['GET', 'POST'])
def page_booking():
    data_seed()

    booking = BookingForm(request.form)
    booking.date.data = get_date_tomorrow()
    booking.site.choices = get_all_dive_sites_options()
    
    return render_template('booking/booking.html', form = booking)

@blueprint.route('/test', methods=['GET', 'POST'])
def page_test():
    return render_template('home/form_elements.html')