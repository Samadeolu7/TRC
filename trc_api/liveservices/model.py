from sqlalchemy import Date
import trc_api.database as models

db = models.db
ma = models.ma

class LiveService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(Date)
    url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean)

    def delete_outdated_events(self):
        outdated_events = LiveService.query.filter(LiveService.date < LiveService.now()).all()
        for event in outdated_events:
            db.session.delete(event)
        db.session.commit()


class LiveServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date', 'url', 'is_active')

live_service_schema = LiveServiceSchema()
live_services_schema = LiveServiceSchema(many=True)