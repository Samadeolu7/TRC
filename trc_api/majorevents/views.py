from flask import request
from trc_api.database import db
from flask_restful import Resource, reqparse, fields, marshal_with
from trc_api.liveservices.model import live_services_schema
from trc_api.upcomingevents.model import Events

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'image': fields.String,
    'list_of_guests': fields.String,
    'date': fields.String,
    'url': fields.String
}
