from flask import Flask
from dotenv import load_dotenv
from trc_api.liveservices.model import LiveService
from trc_api.majorevents.model import MajorEvents
from trc_api.upcomingevents.model import MajorService, Event
from trc_api.cluster.model import Cluster, Question
import os
from trc_api.database import ma, db

load_dotenv()




class Sermons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(db.String(200))
    url = db.Column(db.String(200))
    type = db.Column(db.String(200))
    #sort by date

class LiveServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date', 'url', 'is_active')

live_service_schema = LiveServiceSchema()
live_services_schema = LiveServiceSchema(many=True)


