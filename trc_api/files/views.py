from flask import request, send_file
from flask_restful import Resource
from werkzeug.datastructures import FileStorage
from trc_api.sermons.model import Sermons
from trc_api.database import db
from dotenv import load_dotenv
import os
from flask import current_app

from trc_api.upcomingevents.model import Events, Guest

class GuestImage(Resource):
    
    def get(self, id):
        guest = Guest.query.get(id)

        image_path = guest.image
        if image_path:
            send_file(image_path)
        return {'message': 'The guest does not have an image'}, 404
    

class EventImage(Resource):
    
    def get(self, id):
        event = Events.query.get(id)
        print(event)
        image_path = os.path.join(current_app.root_path, event.image)
        if image_path:
            if os.path.exists(image_path) and os.access(image_path, os.R_OK):
                return send_file(image_path)
            else:
                return {'message': 'The image file cannot be accessed'}, 500
        return {'message': 'The event does not have an image'}, 404
    
class SermonImage(Resource):
        
        def get(self, id):
            sermon = Sermons.query.get(id)
            print(sermon)
            image_path = os.path.join(current_app.root_path, sermon.image)
            if image_path:
                if os.path.exists(image_path) and os.access(image_path, os.R_OK):
                    return send_file(image_path)
                else:
                    return {'message': 'The image file cannot be accessed'}, 500
            return {'message': 'The sermon does not have an image'}, 404