from flask import Flask
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from models import LiveService, live_services_schema,MajorService,Event,Sermons,MajorEvents
from models import db
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
import os

load_dotenv()


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

api = Api(app)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'url': fields.String,
    'is_active': fields.Boolean
}

class LiveServiceList(Resource):
    def get(self):
        live_services = LiveService.query.all()
        return live_services_schema.dump(live_services)
    
     
    @marshal_with(resource_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        data = parser.parse_args()
        
        new_live_service = LiveService(
            name=data['name'],
            description=data['description'],
            url=data['url'],
            is_active=data['is_active']
        )
        db.session.add(new_live_service)
        db.session.commit()
        return live_services_schema.dump(new_live_service)
    
     
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        data = parser.parse_args()
        
        live_service = LiveService.query.get(data['id'])
        if live_service:
            db.session.delete(live_service)
            db.session.commit()
            return {
                'message': 'The live service has been deleted'
            }
        return {
            'message': 'The live service does not exist'
        }
    
     
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        data = parser.parse_args()
        
        live_service = LiveService.query.get(data['id'])
        if live_service:
            live_service.name = data['name']
            live_service.description = data['description']
            live_service.url = data['url']
            live_service.is_active = data['is_active']
            db.session.commit()
            return live_services_schema.dump(live_service)
        return {
            'message': 'The live service does not exist'
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

class UpcomingServicesList(Resource):
    def get(self):
        upcoming_services = MajorService.query.all()
        return live_services_schema.dump(upcoming_services)
    
     
    @marshal_with(resource_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('day', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        data = parser.parse_args()
        
        new_upcoming_service = MajorService(
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
        
        upcoming_service = MajorService.query.get(data['id'])
        if upcoming_service:
            db.session.delete(upcoming_service)
            db.session.commit()
            return {
                'message': 'The upcoming service has been deleted'
            }
        return {
            'message': 'The upcoming service does not exist'
        }
    
     
    @marshal_with(resource_fields)
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
    
@app.route('/api-guide', methods=['GET'])
class ApiGuide(Resource):
    def get(self):
        guide = {
            "/liveservices": {
                "GET": "Returns a list of all live services",
                "POST": "Creates a new live service",
                "DELETE": "Deletes a live service",
                "PUT": "Updates a live service"
            },
            "/majorevents": {
                "GET": "Returns a list of all major events",
                "POST": "Creates a new major event",
                "DELETE": "Deletes a major event",
                "PUT": "Updates a major event"
            },
            "/upcomingevents": {
                "GET": "Returns a list of all upcoming services",
                "POST": "Creates a new upcoming service",
                "DELETE": "Deletes an upcoming service",
                "PUT": "Updates an upcoming service"
            }
        }
        return guide
    
api.add_resource(LiveServiceList, '/liveservices')
api.add_resource(MajorEventsList, '/majorevents')
api.add_resource(UpcomingServicesList, '/upcomingevents')
api.add_resource(ApiGuide, '/api-guide')


if __name__ == '__main__':
    app.run(debug=True)