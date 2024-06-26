from trc_api.database import db
from flask_restful import Resource, reqparse, fields, marshal_with
from trc_api.majorevents.model import MajorEvents
from trc_api.liveservices.model import live_services_schema

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'image': fields.String,
    'list_of_guests': fields.String,
    'date': fields.String,
    'url': fields.String
}


class MajorEventsList(Resource):
    def get(self):
        major_events = MajorEvents.query.all()
        return live_services_schema.dump(major_events)
    
     
    @marshal_with(resource_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('image', type=str, required=True)
        parser.add_argument('list_of_guests', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        data = parser.parse_args()
        
        new_major_event = MajorEvents(
            name=data['name'],
            description=data['description'],
            image=data['image'],
            list_of_guests=data['list_of_guests'],
            date=data['date'],
            url=data['url']
        )
        db.session.add(new_major_event)
        db.session.commit()
        return live_services_schema.dump(new_major_event)
    
     
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        data = parser.parse_args()
        
        major_event = MajorEvents.query.get(data['id'])
        if major_event:
            #delete all guests
            for guest in major_event.list_of_guests:
                db.session.delete(guest)
            db.session.delete(major_event)
            db.session.commit()
            return {
                'message': 'The major event has been deleted'
            }
        return {
            'message': 'The major event does not exist'
        }
    
     
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('image', type=str, required=True)
        parser.add_argument('list_of_guests', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        data = parser.parse_args()
        
        major_event = MajorEvents.query.get(data['id'])
        if major_event:
            major_event.name = data['name']
            major_event.description = data['description']
            major_event.image = data['image']
            major_event.list_of_guests = data['list_of_guests']
            major_event.date = data['date']
            major_event.url = data['url']
            db.session.commit()
