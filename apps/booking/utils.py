from datetime import datetime, timedelta
from apps.booking.models import Dive_Site

def get_all_dive_sites():
    return Dive_Site.query.all()    

def get_date_tomorrow():
    """
    Return a date object for tomorrow.
    """
    return datetime.now() + timedelta(days=1)


