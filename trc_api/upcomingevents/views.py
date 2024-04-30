from datetime import datetime, timedelta
from flask_restful import Resource, reqparse
from flask import request
from trc_api.database import db, photos
from trc_api.majorevents.model import Guest, MajorEvents
from trc_api.upcomingevents.model import MajorService, Events, upcoming_events_schema
from werkzeug.utils import secure_filename
from trc_api.liveservices.model import LiveService, live_services_schema


class UpcomingEventList(Resource):
    def get(self):
        upcoming_services = Events.query.filter(Events.date >= datetime.now(), Events.date <= datetime.now() + timedelta(days=30)).all()

        upcoming_services += MajorEvents.query.filter(MajorEvents.date >= datetime.now(), MajorEvents.date <= datetime.now() + timedelta(days=90)).all()
        

        return upcoming_events_schema.dump(upcoming_services)
    
     
    # @marshal_with(resource_fields

    def post(self):
        data = request.form
        major = data['major_event']
        guests = data['guests']
        guest_list = []
        for guest in guests:
            new_guest = Guest(
                name=guest['name'],
                image=guest['image'],
                major_event_id=guest['major_event_id']
            )
            db.session.add(new_guest)
            guest_list.append(new_guest)

        # Save the uploaded image
        image = request.files['image']
        filename = photos.save(image)
        filepath = 'uploads/' + filename

        if major:
            
            new_upcoming_service = MajorEvents(
                name=data['name'],
                description=data['description'],
                day=data['date'],
                time=data['time'],
                url=data['url'],
                image=filepath,  # Save the file path to the database
                guests=guest_list
            )
        else:
            new_upcoming_service = Events(
                name=data['name'],
                description=data['description'],
                day=data['date'],
                time=data['time'],
                url=data['url'],
                image=filepath,  # Save the file path to the database
                guests=guest_list
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
            upcoming_service = MajorEvents.query.get(data['id'])
        else:
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
            upcoming_service.day = data['day']
            upcoming_service.time = data['time']
            db.session.commit()
            return live_services_schema.dump(upcoming_service)
        return {
            'message': 'The upcoming service does not exist'
        }
    

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
                day=data['day'],
                time=data['time']
            )
        else:
            new_upcoming_service = LiveService(
                name=data['name'],
                description=data['description'],
                day=data['day'],
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
            upcoming_service.day = data['day']
            upcoming_service.time = data['time']
            db.session.commit()
            return live_services_schema.dump(upcoming_service)
        return {
            'message': 'The upcoming service does not exist'
        }
    
