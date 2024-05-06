from sqlalchemy import Date
from trc_api.database import db, ma
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
from flask import url_for
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from dotenv import load_dotenv
import os

load_dotenv()

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image_url = db.Column(db.String(200), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def delete_if_not_associated(self):
        if self.major_event_id is None and self.event_id is None:
            db.session.delete(self)
            db.session.commit()
            
class MajorService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(Date)
    time = db.Column(db.String(200))

    def increment_date(self):
        self.date = self.date + timedelta(days=7)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    date = db.Column(Date)
    time = db.Column(db.String(200))
    url = db.Column(db.String(200))
    guests = db.relationship('Guest', backref='event')
    major_event = db.Column(db.Boolean, default=False)

    #delete oudated events
    def delete_outdated_events(self):
        outdated_events = Events.query.filter(Events.date < datetime.now()).all()
        for event in outdated_events:
            db.session.delete(event)
        db.session.commit()

class UpcomingEventsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Events
        include_fk = True

    image_url = fields.Method('get_image_url')

    def get_image_url(self, obj):
        base_url = os.getenv('BASE_URL')
        return f'{base_url}events/{obj.id}'


class UpcomingMEventsSchema(SQLAlchemyAutoSchema):
    base_url = os.getenv('BASE_URL')
    class Meta:
        model = Events
        include_fk = True

    image_url = fields.Method('get_image_url')

    def get_image_url(self, obj):
        base_url = os.getenv('BASE_URL')
        return f'{base_url}events/{obj.id}'




class GuestSchema(SQLAlchemyAutoSchema):
    base_url = os.getenv('BASE_URL')
    class Meta:
        model = Guest
        include_fk = True


    image_url = fields.Method('get_image_url')

    def get_image_url(self, obj):
        base_url = os.getenv('BASE_URL')
        return f'{base_url}guests/{obj.id}'
