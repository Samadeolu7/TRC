from flask_restful import Resource, marshal_with, reqparse, fields

from models import LiveService, live_service_schema, live_services_schema, db


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
        return live_service_schema.dump(live_services)
    
     
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
        return live_service_schema.dump(new_live_service)
    
     
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
