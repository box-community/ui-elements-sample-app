"""
functions to help with templates
"""

from xmlrpc.client import boolean
from apps.booking.utils import get_all_dive_sites
from apps.booking.models import Booking_Diver
from apps import db


def get_all_dive_sites_options():
    """
    Return a list of tuples with the dive site id and name.
    """

    mylist = get_all_dive_sites()

    options = []
    for row in mylist:
        options.append((row.id, row.name))

    options.insert(0, ('', 'Select a dive site'))

    return options

def booking_diver_upload_process(data)->boolean:
    """
    Process the upload of a certificate or insurance car for a booking diver.
    """

    if data['eventType'] == 'complete':
        if data['documentType'] == 'CERTIFICATE':
            if data['e'][0]['type'] == 'file':
                if data['e'][0]['id'] is not None:
                    booking_diver = Booking_Diver.query.filter_by(id=data['booking_diver_id']).first()
                    booking_diver.certification_file_id = data['e'][0]['id']
                    db.session.commit()
                    return True
        elif data['documentType'] == 'INSURANCE':
            if data['e'][0]['type'] == 'file':
                if data['e'][0]['id'] is not None:
                    booking_diver = Booking_Diver.query.filter_by(id=data['booking_diver_id']).first()
                    booking_diver.insurance_file_id = data['e'][0]['id']
                    db.session.commit()
                    return True
    
    return False



