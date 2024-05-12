from datetime import datetime
from flask import current_app, request, send_file
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
        save_path = os.getcwd() + '/trc_api/upload/sermons'
        audio_file.save(save_path +'/audio/'+ audio_file.filename)
        audio = MP3(audio_file)
        audio_len = audio.info.length
        image.save(save_path +'/image/'+ image.filename)

        date_str = request.form['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        name = request.form['name']
        description = request.form['description']
        speaker = request.form['speaker']
        speaker_description = request.form['speaker_description']
        type = request.form['type']
        try:
            sermon = Sermons(
                name=name,
                description=description,
                speaker=speaker,
                date=date_obj,  # assuming date is in 'YYYY-MM-DD' format
                speaker_desription=speaker_description,  # corrected field name
                audio_file=os.path.join(save_path, 'audio', audio_file.filename),  # corrected file path
                image=os.path.join(save_path, 'image', image.filename),  # corrected file path
                audio_len=int(audio_len),
                type=type,
            )
            
            db.session.add(sermon)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'message': 'An error occurred while adding the sermon'}, 500

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
                os.remove(os.path.join(current_app.root_path, sermon.audio_file))
                os.remove(os.path.join(current_app.root_path, sermon.image))
                db.session.delete(sermon)
                db.session.commit()
                return {'message': 'Sermon has been deleted'}, 200
            return {'message': 'Sermon not found'}, 404
        
        def put(self, id):
            sermon = Sermons.query.get(id)
            if sermon:
                data = request.form
                files = request.files
                save_path = os.getcwd() + '/trc_api/upload/sermons'
                if 'audio_file' in files:
                    # Delete the old audio file
                    os.remove(sermon.audio_file)
                    # Save the new audio file
                    audio_file = files['audio_file']
                    audio_file.save(save_path +'/audio/'+ audio_file.filename)
                    audio = MP3(save_path +'/audio/'+ audio_file.filename)
                    sermon.audio_len = audio.info.length
                    sermon.audio_file = save_path +'/audio/'+ audio_file.filename
                if 'image' in files:
                    # Delete the old image file
                    os.remove(sermon.image)
                    # Save the new image file
                    image = files['image']
                    image.save(save_path +'/image/'+ image.filename)
                    sermon.image = save_path +'/image/'+ image.filename
                if 'name' in data:
                    sermon.name = data['name']
                if 'description' in data:
                    sermon.description = data['description']
                if 'speaker' in data:
                    sermon.speaker = data['speaker']
                if 'speaker_description' in data:
                    sermon.speaker_description = data['speaker_description']
                if 'date' in data:
                    date_str = data['date']
                    date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                    sermon.date = date_obj
                if 'type' in data:
                    sermon.type = data['type']
                db.session.commit()
                return {'message': 'Sermon has been updated'}, 200
            return {'message': 'Sermon not found'}, 404

class SermonDownload(Resource):
    
    def get(self, sermon_id):
        sermon = Sermons.query.get(sermon_id)
        if sermon:
            return send_file(sermon.path, as_attachment=True)
        return {'message': 'Sermon not found'}, 404
    