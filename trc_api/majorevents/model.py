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
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def delete_if_not_associated(self):
        if self.major_event_id is None and self.event_id is None:
            db.session.delete(self)
            db.session.commit()
