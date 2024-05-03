from flask import request, send_file
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from trc_api.sermons.model import Sermons
from trc_api.database import db
from dotenv import load_dotenv
import os

load_dotenv()

class Sermon(Resource):

    def get(self):
        sermons = Sermons.query.all()
        return {'sermons': [(sermon.id,sermon.name,sermon.type) for sermon in sermons]}, 200

    def post(self):
        # Check if the post request has the file part
        if 'file' not in request.files:
            return {'message': 'No file part in the request'}, 400

        file = request.files['file']

        # If the user does not select a file, the browser might
        # submit an empty file part without a filename, so check this
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        # You can now use the file object
        # For example, to save it to a file in the server:
        save_path = os.path.join(os.getcwd(), 'sermons')
        file.save(save_path + file.filename)
        
        sermon = Sermons(
            name=request.form['name'],
            description=request.form['description'],
            speaker=request.form['speaker'],
            date=request.form['date'],
            length= request.form['length'],
            path=save_path + file.filename
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
    
        def get(self, sermon_id):
            sermon = Sermons.query.get(sermon_id)
            if sermon:
                return {'sermon': {'id': sermon.id, 'name': sermon.name, 'description': sermon.description, 'speaker': sermon.speaker, 'date': sermon.date, 'path': sermon.path}}, 200
            return {'message': 'Sermon not found'}, 404
    
        def delete(self, sermon_id):
            sermon = Sermons.query.get(sermon_id)
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
    