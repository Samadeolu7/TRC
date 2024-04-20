from trc_api.database import db, ma


class MajorEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date = db.Column(db.String(200))
    url = db.Column(db.String(200))
    guests = db.relationship('Guest', backref='major_event')


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    major_event_id = db.Column(db.Integer, db.ForeignKey('major_events.id'))
