from apps.booking.models import Dive_Site
from apps import db


def data_seed():
    """
    Seed the database with some data.
    """
    # Insert dive site data

    site = Dive_Site.query.all()
    # apps/static/assets

    if not site:
        dive_site1 = Dive_Site(name="Ras Mohamed", picture_url="/images/sites/01-ras-mohamed.jpg")
        dive_site2 = Dive_Site(name="Thistlegorm", picture_url="/images/sites/02-thistlegorm.jpg")
        dive_site3 = Dive_Site(name="Sharks Bay", picture_url="/images/sites/03-shark-bay.jpg")
        dive_site4 = Dive_Site(name="Eagle Ray Bay", picture_url="/images/sites/04-eagle-ray-bay.jpg")
        dive_site5 = Dive_Site(name="Cenotes", picture_url="/images/sites/05-cenotes.jpg")
        dive_site6 = Dive_Site(name="Tropicana", picture_url="/images/sites/06-tropicana.jpg")
        db.session.add(dive_site1)
        db.session.add(dive_site2)
        db.session.add(dive_site3)
        db.session.add(dive_site4)
        db.session.add(dive_site5)
        db.session.add(dive_site6)
        db.session.commit()
