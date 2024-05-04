import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_uploads import UploadSet, configure_uploads, IMAGES

ma = Marshmallow()
load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Create different UploadSet instances for different types of photos
guest_photos = UploadSet('guestsphotos', IMAGES)
event_photos = UploadSet('eventphotos', IMAGES)
sermon_photos = UploadSet('sermonphotos', IMAGES)
sermon_speaker_photos = UploadSet('sermonspeakerphotos', IMAGES)


def configure_upload_sets(app):
    # Configure the upload sets
    app.config['UPLOADED_GUESTSPHOTOS_DEST'] = 'trc_api/upload/guests'
    app.config['UPLOADED_EVENTPHOTOS_DEST'] = 'trc_api/upload/events'
    app.config['UPLOADED_SERMONPHOTOS_DEST'] = 'trc_api/upload/sermons'
    app.config['UPLOADED_SERMONSPEAKERPHOTOS_DEST'] = 'trc_api/upload/sermon_speakers'

    configure_uploads(app, (guest_photos, event_photos, sermon_photos, sermon_speaker_photos))


# Initialize the database
db = SQLAlchemy()
db.init_app(app)