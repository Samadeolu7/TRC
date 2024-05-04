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

class GuestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Guest
        include_fk = True

    image_url = fields.Method('get_image_url')

    def get_image_url(self, obj):
        if obj.image is not None:
            return url_for('static', filename=obj.image, _external=True)
        else:
            return None

