from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import Email, DataRequired


class BookingForm(FlaskForm):

    date = DateField('Date',
                     validators=[DataRequired()],
                     id='date_booking',
                     default = (datetime.today),
                     )

    site = SelectField(name='site',
                       label='Dive site',
                       id='site_booking',
                       validators=[DataRequired()])

    name = StringField('Name',
                       id='name_booking',
                       validators=[DataRequired()])

    email = StringField('Email',
                        id='email_booking',
                        validators=[DataRequired(), Email()])


class DiverForm(FlaskForm):
    name = StringField('Name',
                       id='name_booking',
                       validators=[DataRequired()])

    email = StringField('Email',
                        id='email_booking',
                        validators=[DataRequired(), Email()])

class BookingSimpleForm(FlaskForm):
    date = DateField('Date',
                     validators=[DataRequired()],
                     id='date_booking',
                     default = (datetime.today),
                     )
    site = StringField(name='site',
                       label='Dive site',
                       id='site_booking',
                       validators=[DataRequired()])
