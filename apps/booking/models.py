from datetime import datetime
from apps import db

class Dive_Site(db.Model):
    __tablename__ = 'Dive_Site'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
                # depending on whether value is an iterable or not, we must
                # unpack it's value (when **kwargs is request.form, some values
                # will be a 1-element list)
                if hasattr(value, '__iter__') and not isinstance(value, str):
                    # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                    value = value[0]

                setattr(self, property, value) 

    def __repr__(self):
        return str(self.name)



class Diver(db.Model):
    __tablename__ = 'Diver'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=False, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
                # depending on whether value is an iterable or not, we must
                # unpack it's value (when **kwargs is request.form, some values
                # will be a 1-element list)
                if hasattr(value, '__iter__') and not isinstance(value, str):
                    # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                    value = value[0]

                setattr(self, property, value) 

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

class Booking(db.Model):
    __tablename__ = 'Booking'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    dive_site_id = db.Column(db.Integer, db.ForeignKey('Dive_Site.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True)
    # box_folder_id = db.Column(db.String(500), unique=True, nullable=True)


    def __init__(self, **kwargs):

        for property, value in kwargs.items():
                # depending on whether value is an iterable or not, we must
                # unpack it's value (when **kwargs is request.form, some values
                # will be a 1-element list)
                if hasattr(value, '__iter__') and not isinstance(value, str):
                    # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                    value = value[0]

                setattr(self, property, value)        


    def __repr__(self):
        return "<TableName(id='%s')>" % self.id

class Booking_Diver(db.Model):
    __tablename__ = 'Booking_Diver'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('Booking.id'), nullable=False)
    diver_id = db.Column(db.Integer, db.ForeignKey('Diver.id'), nullable=False)
    

    def __init__(self, **kwargs):

        for property, value in kwargs.items():
                # depending on whether value is an iterable or not, we must
                # unpack it's value (when **kwargs is request.form, some values
                # will be a 1-element list)
                if hasattr(value, '__iter__') and not isinstance(value, str):
                    # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                    value = value[0]

                setattr(self, property, value) 

    def __repr__(self):
        return "<TableName(id='%s')>" % self.id