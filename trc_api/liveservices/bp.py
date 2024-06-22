# In a new file, e.g., major_events.py
from flask import Blueprint
from flask_restful import Api
from .views import LiveServiceList, LiveServiceEdit, CurrentLiveService

liveservices_bp = Blueprint('liveservice', __name__)
api = Api(liveservices_bp)

api.add_resource(LiveServiceList, '/services')
api.add_resource(LiveServiceEdit, '/services/<int:id>')
api.add_resource(CurrentLiveService, '/services/live')