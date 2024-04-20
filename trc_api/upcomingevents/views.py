from flask_restful import Resource, reqparse, fields, marshal_with
from trc_api.models import db
from trc_api.upcomingevents.model import MajorService
from trc_api.liveservices.model import LiveService, live_services_schema


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'day': fields.String,
    'time': fields.String
}



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