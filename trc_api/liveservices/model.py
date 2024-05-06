from datetime import timedelta
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Date
import trc_api.database as models

db = models.db
ma = models.ma

class LiveService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(Date)
    time = db.Column(db.String(200))
    url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=False)
    speaker = db.Column(db.String(100))

    def delete_outdated_events(self):
        outdated_events = LiveService.query.filter(LiveService.date < LiveService.now()).all()
        for event in outdated_events:
            db.session.delete(event)
        db.session.commit()


class MajorService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(Date)
    time = db.Column(db.String(200))
    url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=False)
    speaker = db.Column(db.String(100))
    

    def increment_date(self):
        self.date = self.date + timedelta(days=7)

class LiveServiceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = LiveService
        load_instance = True
    

live_service_schema = LiveServiceSchema()
live_services_schema = LiveServiceSchema(many=True)