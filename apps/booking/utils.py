from datetime import datetime, timedelta
from apps.booking.models import Dive_Site
from apps.config import Config

from boxsdk.object.user import User


def get_all_dive_sites():
    return Dive_Site.query.all()


def get_date_tomorrow():
    """
    Return a date object for tomorrow.
    """
    return datetime.now() + timedelta(days=1)


def get_task_user(client) -> User:
    """
    Return the task user object.
    """
    return client.user(user_id=Config.TASK_USER_LOGIN).get()
