""" boot strap application with seed data, files, box structure, etc. """

from apps.authentication.box_jwt import jwt_check_client
from apps.booking.demo_folders import site_folder_get
from apps.booking.models import Dive_Site
from apps.booking.data_seed import data_seed
from apps.home.demo_files import collaborate_demo_folder, create_demo_folder, upload_demo_files


def boot_strap():
    client = jwt_check_client()
    create_demo_folder(client)
    collaborate_demo_folder(client)

    data_seed()

    sites = Dive_Site.query.all()

    # create each dive site folder in box
    for site in sites:
        site_folder_get(site.id)

    # upload dmeo files
    upload_demo_files(client)
