from flask import request, send_file
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from trc_api.sermons.model import Sermons, SermonsSchema
from trc_api.database import db
from dotenv import load_dotenv
from mutagen.mp3 import MP3
import os


load_dotenv()

class Sermon(Resource):

    def get(self):
        sermons = Sermons.query.all()
        sermons_schema = SermonsSchema(many=True)
        return sermons_schema.dump(sermons), 200

    def post(self):
        if 'audio_file' not in request.files or 'image' not in request.files:
            return {'message': 'No file part'}, 400

        audio_file = request.files['audio_file']
        image = request.files['image']


        if audio_file.filename == '':
            return {'message': 'No selected file'}, 400
        if image.filename == '':
            return {'message': 'No selected file'}, 400
        save_path = os.path.join(os.getcwd(), 'sermons')
        audio_file.save(save_path +'/audio/'+ audio_file.filename)
        audio = MP3(save_path +'/audio/'+ audio_file.filename)
        audio_len = audio.info.length
        image.save(save_path +'/image/'+ image.filename)
        
        sermon = Sermons(
            name=request.form['name'],
            description=request.form['description'],
            speaker=request.form['speaker'],
            date=request.form['date'],
            speaker_description = request.form['speaker_description'],
            audio_file=save_path + audio_file.filename,
            image=save_path + image.filename,
            audio_len=int(audio_len),
            type=request.form['type'],
        )
        sermon_count = Sermons.query.count()
        sermon_limit = int(os.getenv('SERMON_LIMIT'))
        # Check if the limit has been reached
        if sermon_count >= sermon_limit:
            # If the limit is reached, delete the oldest sermon
            oldest_sermon = Sermons.query.order_by(Sermons.date).first()
            db.session.delete(oldest_sermon)
        db.session.add(sermon)
        db.session.commit()

        return {'message': 'Sermon has been added'}, 201
    

class SermonDetail(Resource):
    
        def get(self, id):
            sermon = Sermons.query.get(id)
            if sermon:
                sermon_schema = SermonsSchema()
                return sermon_schema.dump(sermon), 200
            
            return {'message': 'Sermon not found'}, 404
    
        def delete(self,id):
            sermon = Sermons.query.get(id)
            if sermon:
                os.remove(sermon.path)
                db.session.delete(sermon)
                db.session.commit()
                return {'message': 'Sermon has been deleted'}, 200
            return {'message': 'Sermon not found'}, 404
        

class SermonDownload(Resource):
    
    def get(self, sermon_id):
        sermon = Sermons.query.get(sermon_id)
        if sermon:
            return send_file(sermon.path, as_attachment=True)
        return {'message': 'Sermon not found'}, 404
    