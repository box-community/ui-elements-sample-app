

from datetime import date
import os
from boxsdk import BoxAPIException, Client
from boxsdk.object.folder import Folder
from apps.config import Config
from apps import db
from apps.booking.models import Booking, Booking_Diver, Diver, Dive_Site
from apps.authentication.models import Jwt
from apps.authentication.box_jwt import jwt_check_client, jwt_client


def folder_non_root_exists(folder_id:str = '0')->bool:
	"""
	checks if the folder exists as a subfolder of the root folder
	"""
	if folder_id is None or folder_id == '0':
		return False

	client = jwt_check_client()

	try:
		client.folder(folder_id).get()

	except BoxAPIException as error:
		if error.status == 404:
			return False
		raise error
	
	return True

def demo_folder_create(client:Client)->str:

	# try to create the demo folder in root
	try:
		demo_folder_id = client.folder(0).create_subfolder(Config.DEMO_FOLDER_NAME).id
	except BoxAPIException as error:
		demo_folder_id = error.context_info['conflicts'][0]['id']

	jwt_rec = Jwt.query.filter_by(box_app_id = Config.JWT_PUBLIC_KEY_ID).first()
	jwt_rec.box_demo_folder_id = demo_folder_id
	db.session.commit()
	return demo_folder_id

def demo_folder_get(client:Client)->str:
	jwt_rec = Jwt.query.filter_by(box_app_id = Config.JWT_PUBLIC_KEY_ID).first()

	if folder_non_root_exists(jwt_rec.box_demo_folder_id):
		return jwt_rec.box_demo_folder_id
	
	return demo_folder_create(client)








def site_folder_create(site_id:int)->str:
	"""
	creates the folder for the site
	"""
	site = Dive_Site.query.filter_by(id=site_id).first()
	
	if site is None:
		return None
	
	client = jwt_check_client()

	demo_folder_id = demo_folder_get(client)

	# try to create the demo folder in demo_folder (bookings)
	try:
		folder_id = client.folder(demo_folder_id).create_subfolder(site.name).id
	except BoxAPIException as error:
		folder_id = error.context_info['conflicts'][0]['id']
	
	site.box_folder_id = folder_id
	db.session.commit()
	return folder_id

def site_folder_get(site_id:int)->str:
	"""
	returns the folder id for the site
	"""
	folder_id = Dive_Site.query.filter_by(id=site_id).first().folder_id
	
	if folder_non_root_exists(folder_id):
		return folder_id
	
	return site_folder_create(site_id)





def booking_folder_create(booking_id:int)->str:
	"""
	creates the folder for the booking
	"""
	booking = Booking.query.filter_by(id=booking_id).first()
	
	if booking is None:
		raise Exception('booking not found')

	# get site folder
	site_folder_id = site_folder_get(booking.dive_site_id)

	client = jwt_check_client()

	# try to create the booking folder in site_folder
	try:
		folder_id = client.folder(site_folder_id).create_subfolder(booking.date.strftime('%Y-%m-%d')).id
	except BoxAPIException as error:
		folder_id = error.context_info['conflicts'][0]['id']
	
	booking.folder_id = folder_id
	db.session.commit()

	return folder_id

def booking_folder_get(booking_id:int)->str:
	"""
	returns the folder id for the booking
	"""
	folder_id = Booking.query.filter_by(id=booking_id).first().folder_id

	if folder_non_root_exists(folder_id):
		return folder_id

	folder_id = booking_folder_create(booking_id)
	
	return folder_id
	

def booking_diver_folder_create(booking_diver_id:int)->str:
	"""
	creates the folder for the booking diver
	"""
	booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()
	diver = Diver.query.filter_by(id=booking_diver.diver_id).first()
	
	if booking_diver is None:
		raise Exception('booking diver not found')
	
	if diver is None:
		raise Exception('diver not found')

	booking_folder_id = booking_folder_get(booking_diver.booking_id)
	
	client = jwt_check_client()

	# try to create the booking folder in booking_folder
	try:
		folder_id = client.folder(booking_folder_id).create_subfolder(diver.name).id
	except BoxAPIException as error:
		folder_id = error.context_info['conflicts'][0]['id']
	
	booking_diver.folder_id = folder_id
	db.session.commit()

	return folder_id

def booking_diver_folder_get(booking_diver_id:int)->str:
	"""
	returns the folder id for the booking diver
	"""
	booking_diver = Booking_Diver.query.filter_by(id=booking_diver_id).first()
	
	if booking_diver is None:
		raise Exception('booking diver not found')

	if folder_non_root_exists(booking_diver.folder_id):
		return booking_diver.folder_id

	booking_diver_folder_id = booking_diver_folder_create(booking_diver_id)

	return booking_diver_folder_id




