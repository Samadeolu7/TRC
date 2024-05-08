from flask import Blueprint
from flask_restful import Api
from .views import GuestImage, EventImage, SermonImage, SermonAudio

files_bp = Blueprint('files', __name__)
api = Api(files_bp)

api.add_resource(GuestImage, '/upload/guests/<int:id>')
api.add_resource(EventImage, '/upload/events/<int:id>')
api.add_resource(SermonImage, '/upload/sermons/<int:id>/image')
api.add_resource(SermonAudio, '/upload/sermons/<int:id>/audio')