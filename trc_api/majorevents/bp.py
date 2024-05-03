# In a new file, e.g., major_events.py
from flask import Blueprint
from flask_restful import Api

major_events_bp = Blueprint('major_events', __name__)
api = Api(major_events_bp)
