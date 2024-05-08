from sqlalchemy import Date
from trc_api.database import db, ma
from marshmallow import fields
import os

class Sermons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    speaker = db.Column(db.String(200))
    speaker_desription = db.Column(db.String(200))
    date = db.Column(Date)
    audio_file = db.Column(db.String(200))
    image = db.Column(db.String(200))
    type = db.Column(db.String(200))

class SermonsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sermons
        load_instance = True
        include_fk = True

    image_url = fields.Method('get_image_url')
    audio_file_url = fields.Method('get_audio_url')

    def get_image_url(self, obj):
        base_url = os.getenv('BASE_URL')
        return f'{base_url}sermons/{obj.id}'
    
    def get_audio_url(self, obj):
        base_url = os.getenv('BASE_URL')
        return f'{base_url}semons/{obj.id}'