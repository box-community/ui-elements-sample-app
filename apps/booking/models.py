from datetime import datetime
import hashlib
from apps import db


class Dive_Site(db.Model):
    __tablename__ = "Dive_Site"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True, nullable=False)
    folder_id = db.Column(db.String(500), unique=True, nullable=True)
    picture_url = db.Column(db.String(500), unique=False, nullable=True)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)


class Diver(db.Model):
    __tablename__ = "Diver"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=False, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    avatar_url = db.Column(db.String(512))

    def __init__(self, **kwargs):
        email = kwargs.get("email")
        avatar_url = kwargs.get("avatar_url")
        if avatar_url is None:
            avatar_url = (
                "https://www.gravatar.com/avatar/"
                + hashlib.md5(email.lower().encode("utf-8")).hexdigest()
                + "?d=identicon"
            )
            setattr(self, "avatar_url", avatar_url)

        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id


class Booking(db.Model):
    __tablename__ = "Booking"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    dive_site_id = db.Column(db.Integer, db.ForeignKey("Dive_Site.id"), nullable=False)
    folder_id = db.Column(db.String(50), unique=True, nullable=True)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id


class Booking_Diver(db.Model):
    __tablename__ = "Booking_Diver"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("Booking.id"), nullable=False)
    diver_id = db.Column(db.Integer, db.ForeignKey("Diver.id"), nullable=False)
    folder_id = db.Column(db.String(50), unique=True, nullable=True)

    certification_file_id = db.Column(db.String(50), unique=False, nullable=True)
    certification_task_id = db.Column(db.String(50), unique=False, nullable=True)
    certification_status = db.Column(db.String(50), unique=False, nullable=True)

    insurance_file_id = db.Column(db.String(50), unique=False, nullable=True)
    insurance_task_id = db.Column(db.String(50), unique=False, nullable=True)
    insurance_status = db.Column(db.String(50), unique=False, nullable=True)

    waiver_file_id = db.Column(db.String(50), unique=False, nullable=True)
    waiver_task_id = db.Column(db.String(50), unique=False, nullable=True)
    waiver_status = db.Column(db.String(50), unique=False, nullable=True)

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, "__iter__") and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            setattr(self, property, value)

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id
