from flask_restful import Resource, Api
from flask import blueprints, request, jsonify


class Ping(Resource):
    def get(self):
        return {'message': 'Pong!'}, 200

class ApiGuide(Resource):
    def get(self):
        guide = {
            'ping': 'Check if the server is up',
            'upcoming_services': 'Get all upcoming services',
            'upcoming_events': 'Get all upcoming events',
            'major_events': 'Get all major events',     
        }
        return jsonify(guide)
    
ping_bp = blueprints.Blueprint('ping', __name__)
api = Api(ping_bp)
api.add_resource(Ping, '/ping')
api.add_resource(ApiGuide, '/api_guide')
