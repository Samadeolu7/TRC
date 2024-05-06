# In a new file, e.g., major_events.py
from flask import Blueprint
from flask_restful import Api
from trc_api.upcomingevents.views import UpcomingEventList

upcoming_events_bp = Blueprint('upcomingevents', __name__)
api = Api(upcoming_events_bp)

api.add_resource(UpcomingEventList, '/events')