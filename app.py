from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
import os, json
from jsondb import JsonDB
from flask_cors import CORS

load_dotenv()


app = Flask(__name__)

CORS(app) 

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

api = Api(app)


db = JsonDB('data.json')


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'url': fields.String,
    'is_active': fields.Boolean
}

# class LiveServiceList(Resource):
#     def get(self):
#         live_services = LiveService.query.all()
#         return live_services_schema.dump(live_services)

class LiveServiceList(Resource):
    def get(self):
        data = db.read()
        live_services = data['LiveService']
        return jsonify(live_services)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        data = parser.parse_args()

        new_live_service = {
            "id": len(db.read()['LiveService']) + 1,  # Assign new id
            "name": data['name'],
            "description": data['description'],
            "url": data['url'],
            "time": data['time'],
            "date": data['date'],
            "is_active": data['is_active']
        }

        current_data = db.read()
        current_data['LiveService'].append(new_live_service)
        db.write(current_data)

        return new_live_service, 201

    def delete(self,id):

        current_data = db.read()
        live_service = next((item for item in current_data['LiveService'] if item['id'] == id), None)
        if live_service:
            current_data['LiveService'].remove(live_service)
            db.write(current_data)
            return {'message': 'The live service has been deleted'}, 200

        return {'message': 'The live service does not exist'}, 404

    from flask_restful import reqparse

    def put(self, id):
        parser = reqparse.RequestParser()  # initialize parser

        # add arguments to parser
        parser.add_argument('name', required=True)
        parser.add_argument('description', required=True)
        parser.add_argument('url', required=True)
        parser.add_argument('is_active', required=True, type=bool)

        data = parser.parse_args()  # parse incoming request data

        current_data = db.read()
        live_service = next((item for item in current_data['LiveService'] if item['id'] == id), None)
        if live_service:
            live_service['name'] = data['name']
            live_service['description'] = data['description']
            live_service['url'] = data['url']
            live_service['is_active'] = data['is_active']
            db.write(current_data)
            return live_service, 200

        return {'message': 'The live service does not exist'}, 404


class MajorEventsList(Resource):
    #He only needs 3 most prominent major events
    def get(self):
        data = db.read()
        major_events = data['MajorEvents']
        return jsonify(major_events)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('image', type=str, required=True)
        parser.add_argument('guests', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        data = parser.parse_args()

        new_major_event = {
            "id": len(db.read()['MajorEvents']) + 1,  # Assign new id
            "name": data['name'],
            "description": data['description'],
            "image": data['image'],
            "guests": data['guests'],
            "date": data['date'],
            "url": data['url']
        }

        current_data = db.read()
        current_data['MajorEvents'].append(new_major_event)
        db.write(current_data)

        return new_major_event, 201

    def delete(self,id):
        current_data = db.read()
        major_event = next((item for item in current_data['MajorEvents'] if item['id'] == id), None)
        if major_event:
            current_data['MajorEvents'].remove(major_event)
            db.write(current_data)
            return {'message': 'The major event has been deleted'}, 200

        return {'message': 'The major event does not exist'}, 404

    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('image', type=str, required=True)
        parser.add_argument('guests', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        data = parser.parse_args()

        current_data = db.read()
        major_event = next((item for item in current_data['MajorEvents'] if item['id'] == id), None)
        if major_event:
            major_event['name'] = data['name']
            major_event['description'] = data['description']
            major_event['image'] = data['image']
            major_event['guests'] = data['guests']
            major_event['date'] = data['date']
            major_event['url'] = data['url']
            db.write(current_data)
            return major_event, 200

        return {'message': 'The major event does not exist'}, 404

class UpcomingServicesList(Resource):
    def get(self):
        data = db.read()
        upcoming_services = data['UpcomingServices']
        return jsonify(upcoming_services)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('day', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        data = parser.parse_args()

        new_upcoming_service = {
            "id": len(db.read()['UpcomingServices']) + 1,  # Assign new id
            "name": data['name'],
            "description": data['description'],
            "day": data['day'],
            "time": data['time']
        }

        current_data = db.read()
        current_data['UpcomingServices'].append(new_upcoming_service)
        db.write(current_data)

        return new_upcoming_service, 201

    def delete(self, id):
        current_data = db.read()
        upcoming_service = next((item for item in current_data['UpcomingServices'] if item['id'] == id), None)
        if upcoming_service:
            current_data['UpcomingServices'].remove(upcoming_service)
            db.write(current_data)
            return {'message': 'The upcoming service has been deleted'}, 200

        return {'message': 'The upcoming service does not exist'}, 404

    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('day', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        data = parser.parse_args()

        current_data = db.read()
        upcoming_service = next((item for item in current_data['UpcomingServices'] if item['id'] == id), None)
        if upcoming_service:
            upcoming_service['name'] = data['name']
            upcoming_service['description'] = data['description']
            upcoming_service['day'] = data['day']
            upcoming_service['time'] = data['time']
            db.write(current_data)
            return upcoming_service, 200

        return {'message': 'The upcoming service does not exist'}, 404    

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
    
    
api.add_resource(LiveServiceList, '/liveservices', '/liveservices/<int:id>')
api.add_resource(MajorEventsList, '/majorevents', '/majorevents/<int:id>')
api.add_resource(UpcomingServicesList, '/upcomingevents', '/upcomingevents/<int:id>')
api.add_resource(ApiGuide, '/')


if __name__ == '__main__':
    app.run(debug=True)