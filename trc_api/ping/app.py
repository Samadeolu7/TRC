from flask_restful import Resource, Api
from flask import blueprints, request, jsonify


class Ping(Resource):
    def get(self):
        return {'message': 'Pong!'}, 200

ping_bp = blueprints.Blueprint('ping', __name__)
api = Api(ping_bp)
api.add_resource(Ping, '/ping')
