from sqlalchemy import Date
from trc_api.database import db, ma
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime, timedelta

class MajorService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(Date)
    day = db.Column(db.String(200))
    time = db.Column(db.String(200))

    def increment_date(self):
        self.date = self.date + timedelta(days=7)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(Date)

    #delete oudated events
    def delete_outdated_events(self):
        outdated_events = Events.query.filter(Events.date < datetime.now()).all()
        for event in outdated_events:
            db.session.delete(event)
        db.session.commit()

class UpcomingEventsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date')

upcoming_events_schema = UpcomingEventsSchema()

