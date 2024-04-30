from datetime import datetime
from sqlalchemy import Date
from trc_api.database import db, ma
from flask import url_for
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(200), nullable=True)
    major_event_id = db.Column(db.Integer, db.ForeignKey('major_events.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def delete_if_not_associated(self):
        if self.major_event_id is None and self.event_id is None:
            db.session.delete(self)
            db.session.commit()


class MajorEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date = db.Column(Date)
    day = db.Column(db.String(200))
    time = db.Column(db.String(200))
    url = db.Column(db.String(200))
    guests = db.relationship('Guest', backref='major_event')

    def delete_outdated_events(self):
        outdated_events = MajorEvents.query.filter(MajorEvents.date < datetime.now()).all()
        for event in outdated_events:
            db.session.delete(event)
        db.session.commit()

class MajorEventsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = MajorEvents
        include_fk = True

    image_url = fields.Method('get_image_url')

    def get_image_url(self, obj):
        return url_for('static', filename=obj.image, _external=True)



