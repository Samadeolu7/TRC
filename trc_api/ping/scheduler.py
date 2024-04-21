from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from trc_api.upcomingevents.model import MajorService
from trc_api.database import db
from trc_api.majorevents.model import MajorEvents
from trc_api.liveservices.model import LiveService
from trc_api.upcomingevents.model import Events


def update_services():
    services = MajorService.query.all()
    for service in services:
        if service.date <= datetime.today():
            service.increment_date()
    db.session.commit()

def delete_outdated_events():
    events = Events.query.all()
    events += MajorService.query.all()
    events += LiveService.query.all()
    events += MajorEvents.query.all()
    for event in events:
        if event.date <= datetime.today():
            event.delete_outdated_events()
    db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(update_services, 'interval', weeks=1)
scheduler.add_job(delete_outdated_events, 'interval', days=3)
scheduler.start()