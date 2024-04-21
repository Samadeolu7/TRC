from flask import Blueprint
from flask_restful import Api
from .views import Sermon, SermonDetail, SermonDownload

sermons_bp = Blueprint('sermons', __name__)
api = Api(sermons_bp)

api.add_resource(Sermon, '/sermons')
api.add_resource(SermonDetail, '/sermons/<int:id>')
api.add_resource(SermonDownload, '/sermons/download/<int:id>')

