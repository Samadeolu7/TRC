from flask import Blueprint
from flask_restful import Api
from .views import GuestImage, EventImage

files_bp = Blueprint('files', __name__)
api = Api(files_bp)

api.add_resource(GuestImage, '/uploads/guests/<int:id>')
api.add_resource(EventImage, '/uploads/events/<int:id>')