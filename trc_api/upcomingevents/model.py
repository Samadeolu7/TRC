from sqlalchemy import Date
from trc_api.database import db, ma
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta
from flask import url_for
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from trc_api.majorevents.model import Guest, MajorEvents


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
    image = db.Column(db.String(200))
    date = db.Column(Date)
    time = db.Column(db.String(200))
    url = db.Column(db.String(200))
    guests = db.relationship('Guest', backref='event')

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
        return url_for('static', filename=obj.image, _external=True)
    

class UpcomingMEventsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MajorEvents
        include_fk = True

    image_url = fields.Method('get_image_url')

    def get_image_url(self, obj):
        return url_for('static', filename=obj.image, _external=True)
