from apps.booking.models import Dive_Site
from apps import db



def data_seed():
    """
    Seed the database with some data.
    """
    # Insert dive site data

    site = Dive_Site.query.all()

    if not site:
        dive_site1 = Dive_Site(name = 'Test dive site 1')
        dive_site2 = Dive_Site(name = 'Test dive site 2')
        db.session.add(dive_site1)
        db.session.add(dive_site2)
        db.session.commit()

    