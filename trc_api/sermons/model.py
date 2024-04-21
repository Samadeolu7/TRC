from trc_api.database import db, ma

class Sermons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    speaker = db.Column(db.String(200))
    date = db.Column(db.String(200))
    path = db.Column(db.String(200))
    type = db.Column(db.String(200))
    #sort by date