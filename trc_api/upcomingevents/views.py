from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from flask import request
import werkzeug
from trc_api.database import db, guest_photos, event_photos
from trc_api.majorevents.model import Guest
from trc_api.upcomingevents.model import MajorService, Events, UpcomingEventsSchema, UpcomingMEventsSchema
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

        base_url = os.getenv('BASE_URL')
        for event in events_data:
            event['image'] = base_url + f'events/{event["id"]}'
        
        print(events_data)

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
            image = image,
            major_event=int(major)
        )
        db.session.add(new_upcoming_service)
        db.session.commit()
    
        guests = []
        for i in range(2):  # Replace 2 with the actual number of guests
            guest_name = data[f'guests[{i}][name]']
            guest_image = files[f'guests[{i}][image]']
            filename = guest_photos.save(guest_image)
            filepath = 'upload/guests/' + filename
            new_guest = Guest(
                name=guest_name,
                image=filepath,
                event_id=new_upcoming_service.id
            )
            db.session.add(new_guest)
            guests.append(new_guest)
    
        db.session.commit()
    
        upcoming_events_schema = UpcomingEventsSchema()
        return upcoming_events_schema.dump(new_upcoming_service) 
    
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        data = parser.parse_args()
        upcoming_service = Events.query.get(data['id'])
        
        if upcoming_service:
            db.session.delete(upcoming_service)
            db.session.commit()
            return {
                'message': 'The upcoming service has been deleted'
            }
        return {
            'message': 'The upcoming service does not exist'
        }
    
     
    # @marshal_with(resource_fields)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True, location='form')
        parser.add_argument('name', type=str, required=False, location='form')
        parser.add_argument('description', type=str, required=False, location='form')
        parser.add_argument('date', type=str, required=False, location='form')
        parser.add_argument('time', type=str, required=False, location='form')
        parser.add_argument('url', type=str, required=False, location='form')
        parser.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('major_event', type=bool, required=False, location='form')
        data = parser.parse_args()
        files = request.files
    
        upcoming_event = Events.query.get(data['id'])
    
        if upcoming_event:
            if data.get('name'):
                upcoming_event.name = data['name']
            if data.get('description'):
                upcoming_event.description = data['description']
            if data.get('date'):
                upcoming_event.date = data['date']
            if data.get('time'):
                upcoming_event.time = data['time']
            if data.get('url'):
                upcoming_event.url = data['url']
            if data.get('image'):
                image = data['image']
                filename = guest_photos.save(image)
                filepath = 'uploads/' + filename
                upcoming_event.image = filepath
            if data.get('major_event') is not None:
                upcoming_event.major_event = data['major_event']
    
            # Update guests
            for i in range(2):  # Replace 2 with the actual number of guests
                guest_name = data[f'guests[{i}][name]']
                guest_image = files[f'guests[{i}][image]']
                filename = guest_photos.save(guest_image)
                filepath = 'guests/' + filename
                guest = Guest.query.filter_by(event_id=upcoming_event.id, name=guest_name).first()
                if guest:
                    guest.image = filepath
                else:
                    new_guest = Guest(
                        name=guest_name,
                        image=filepath,
                        event_id=upcoming_event.id
                    )
                    db.session.add(new_guest)
    
            db.session.commit()
            upcoming_events_schema = UpcomingEventsSchema(many=True)
            return upcoming_events_schema.dump(upcoming_event)
        else:
            return {'message': 'The upcoming service does not exist'}, 404    

class UpcomingServiceList(Resource):
    def get(self):
        upcoming_services = LiveService.query.filter(LiveService.date >= datetime.now(), LiveService.date <= datetime.now() + timedelta(days=30)).all()

        upcoming_services += MajorService.query.filter(MajorService.date >= datetime.now(), MajorService.date <= datetime.now() + timedelta(days=90)).all()
        

        return live_services_schema.dump(upcoming_services)
    
     
    # @marshal_with(resource_fields)
    def post(self):
        data = request.form
        major = data['major_service']
        if major:
            new_upcoming_service = MajorService(
                name=data['name'],
                description=data['description'],
                date=data['day'],
                time=data['time']
            )
        else:
            new_upcoming_service = LiveService(
                name=data['name'],
                description=data['description'],
                date=data['day'],
                time=data['time']
            )
        db.session.add(new_upcoming_service)
        db.session.commit()
        return live_services_schema.dump(new_upcoming_service)
    
     
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        data = parser.parse_args()
        major = data['major_event']
        if major:
            upcoming_service = MajorService.query.get(data['id'])
        else:
            upcoming_service = LiveService.query.get(data['id'])
        if upcoming_service:
            db.session.delete(upcoming_service)
            db.session.commit()
            return {
                'message': 'The upcoming service has been deleted'
            }
        return {
            'message': 'The upcoming service does not exist'
        }
    
     
    # @marshal_with(resource_fields)
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('day', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        data = parser.parse_args()
        
        upcoming_service = MajorService.query.get(data['id'])
        if upcoming_service:
            upcoming_service.name = data['name']
            upcoming_service.description = data['description']
            # upcoming_service.day = data['day']
            upcoming_service.time = data['time']
            db.session.commit()
            return live_services_schema.dump(upcoming_service)
        return {
            'message': 'The upcoming service does not exist'
        }
    
