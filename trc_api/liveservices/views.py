from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource, marshal_with, reqparse, fields

from trc_api.liveservices.model import LiveService, MajorService, live_service_schema, live_services_schema, db


#TITLE DESCRIPTION URL IS_ACTIVE TIME DATE SPEAKER
class LiveServiceList(Resource):
    def get(self):
        services = LiveService.query.all()
        services += MajorService.query.all()

        return live_services_schema.dump(services)
    
     
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('description', type=str, required=True)
        parser.add_argument('url', type=str, required=True)
        parser.add_argument('is_active', type=bool, required=True)
        parser.add_argument('time', type=str, required=True)
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('speaker', type=str, required=True)
        data = parser.parse_args()

        date_str = data['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        new_live_service = LiveService(
            name=data['name'],
            description=data['description'],
            url=data['url'],
            is_active=data['is_active'],
            time=data['time'],
            date=date_obj,
            speaker=data['speaker']
        )
        db.session.add(new_live_service)
        db.session.commit()
        return live_service_schema.dump(new_live_service)
    

class LiveServiceEdit(Resource):    
    def delete(self,id):
        parser = reqparse.RequestParser()
        data = parser.parse_args()
        
        live_service = LiveService.query.get(id)
        if live_service:
            db.session.delete(live_service)
            db.session.commit()
            return {
                'message': 'The live service has been deleted'
            }
        return {
            'message': 'The live service does not exist'
        }
    
     
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('url', type=str)
        parser.add_argument('is_active', type=bool)
        parser.add_argument('time', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('speaker', type=str)

        data = parser.parse_args()
        
        live_service = LiveService.query.get(id)
        if live_service:
            if data.get('name'):
                live_service.name = data['name']
            if data.get('description'):
                live_service.description = data['description']
            if data.get('url'):
                live_service.url = data['url']
            if data.get('is_active') is not None:
                live_service.is_active = data['is_active']
            if data.get('time'):
                live_service.time = data['time']
            if data.get('date'):
                date_str = data['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                live_service.date = date_obj
            if data.get('speaker'):
                live_service.speaker = data['speaker']
            
            db.session.commit()
            return live_service_schema.dump(live_service)
        return {
            'message': 'The live service does not exist'
        }
    
class CurrentLiveService(Resource):
    def get(self):
        current_date = datetime.now()
        #filter for the on that is active
        services = LiveService.query.filter(LiveService.is_active == True).first()
        major_services = MajorService.query.filter(MajorService.is_active == True).first()
        #return the earliest one
        if services is None and major_services is None:
            return {
                'message': 'No live service available'
            }
        elif services is None:
            return live_service_schema.dump(major_services)
        elif major_services is None:
            return live_service_schema.dump(services)
        if services.date < major_services.date:
            return live_service_schema.dump(services)
        else:
            return live_service_schema.dump(major_services)
