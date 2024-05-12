from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from flask import current_app, request
import werkzeug
from trc_api.database import db, guest_photos, event_photos
from trc_api.upcomingevents.model import Guest, Events, UpcomingEventsSchema, UpcomingMEventsSchema
from werkzeug.utils import secure_filename
from trc_api.liveservices.model import LiveService, live_services_schema
from dotenv import load_dotenv
import os

load_dotenv()


class UpcomingEventList(Resource):
    def get(self):
        upcoming_events = Events.query.all()
        upcoming_events_schema = UpcomingEventsSchema(many=True)
        events_data = upcoming_events_schema.dump(upcoming_events)

        return events_data
    
    def post(self):
        data = request.form
        files = request.files
        major = data['major_event']

        date_str = data['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        image = event_photos.save(files['image'])
        filepath = 'upload/events/' + image
        new_upcoming_service = Events(
            name=data['name'],
            description=data['description'],
            date=date_obj,
            time=data['time'],
            url=data['url'],
            image_url = filepath,
            major_event=int(major)
        )
        db.session.add(new_upcoming_service)
        db.session.commit()

        guests = []
        for i in range(int(data['guests_no'])):  # Replace 2 with the actual number of guests
            guest_name = data[f'guests[{i}][name]']
            guest_image = files[f'guests[{i}][image]']
            filename = guest_photos.save(guest_image)
            filepath = 'upload/guests/' + filename
            new_guest = Guest(
                name=guest_name,
                image_url=filepath,
                event_id=new_upcoming_service.id
            )
            db.session.add(new_guest)
            guests.append(new_guest)
    
        db.session.commit()
    
        upcoming_events_schema = UpcomingEventsSchema()

        res= upcoming_events_schema.dump(new_upcoming_service)
        return res

class UpcomingEventEdit(Resource):
    def get(self, id):
        upcoming_event = Events.query.get(id)
        upcoming_events_schema = UpcomingEventsSchema()
        return upcoming_events_schema.dump(upcoming_event)
    
    def delete(self, id):
        upcoming_service = Events.query.get(id)
        
        if upcoming_service:
            os.remove(os.path.join(current_app.root_path,upcoming_service.image_url))
            for guest in upcoming_service.guests:
                os.remove(os.path.join(current_app.root_path,guest.image_url))
                db.session.delete(guest)
            db.session.delete(upcoming_service)
            db.session.commit()
            return {
                'message': 'The upcoming service has been deleted'
            }
        return {
            'message': 'The upcoming service does not exist'
        }
    
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=False, location='form')
        parser.add_argument('description', type=str, required=False, location='form')
        parser.add_argument('date', type=str, required=False, location='form')
        parser.add_argument('time', type=str, required=False, location='form')
        parser.add_argument('url', type=str, required=False, location='form')
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('major_event', type=bool, required=False, location='form')
        data = parser.parse_args()
        files = request.files

        upcoming_event = Events.query.get(id)
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        if upcoming_event:
            # ... existing if data.get lines ...
            if data.get('name'):
                upcoming_event.name = data['name']
            if data.get('description'):
                upcoming_event.description = data['description']
            if data.get('time'):
                upcoming_event.time = data['time']
            if data.get('url'):
                upcoming_event.url = data['url']
            if data.get('date'):
                date_str = data['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                upcoming_event.date = date_obj

            if data.get('image'):
                image = data['image']
                if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                    os.remove(os.path.join(current_app.root_path, upcoming_event.image_url))  # delete old image
                    filename = guest_photos.save(image)
                    filepath = 'upload/guests/' + filename
                    upcoming_event.image = filepath
                else:
                    return {'message': 'File type not allowed'}, 400

            # Update guests
            # Update guests
            if 'guests' in data:
                existing_guests = {guest.name: guest for guest in upcoming_event.guests}
                for i in range(len(data['guests'])):
                    guest_name = data[f'guests[{i}][name]']
                    guest_image = files[f'guests[{i}][image]']
                    filename = guest_photos.save(guest_image)
                    filepath = 'upload/guests/' + filename
                    if guest_name in existing_guests:
                        os.remove(os.path.join(current_app.root_path, existing_guests[guest_name].image_url))  # delete old image
                        existing_guests[guest_name].image_url = filepath
                    else:
                        new_guest = Guest(
                            name=guest_name,
                            image_url=filepath,
                            event_id=upcoming_event.id
                        )
                        db.session.add(new_guest)

                # Delete guests that are not in the updated list
                for guest_name, guest in existing_guests.items():
                    if guest_name not in [guest['name'] for guest in data['guests']]:
                        os.remove(os.path.join(current_app.root_path, guest.image_url))  # delete image
                        db.session.delete(guest)

            db.session.commit()
            upcoming_events_schema = UpcomingEventsSchema(many=True)
            return upcoming_events_schema.dump(upcoming_event)
        else:
            return {'message': 'The upcoming service does not exist'}, 404