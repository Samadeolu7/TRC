from flask import Flask
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from trc_api.liveservices.model import LiveService
from trc_api.majorevents.model import MajorEvents
from trc_api.upcomingevents.model import MajorService, Event
from trc_api.cluster.model import Cluster, Question
from trc_api.database import db, ma, app

import os


class LiveServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date', 'url', 'is_active')

live_service_schema = LiveServiceSchema()
live_services_schema = LiveServiceSchema(many=True)


with app.app_context():
    db.create_all()
    if LiveService.query.count() == 0:
        new_live_service = LiveService(
            name='Sunday Service',
            description='Sunday Service',
            url='https://www.youtube.com/watch?v=8c7B2v1b5wQ',
            is_active=True
        )
        db.session.add(new_live_service)
        db.session.commit()

        new_live_service = LiveService(
            name='Wednesday Service',
            description='Wednesday Service',
            url='https://www.youtube.com/watch?v=8c7B2v1b5wQ',
            is_active=True
        )
        db.session.add(new_live_service)
        db.session.commit()

        new_live_service = LiveService(
            name='Friday Service',
            description='Friday Service',
            url='https://www.youtube.com/watch?v=8c7B2v1b5wQ',
            is_active=True
        )
        db.session.add(new_live_service)
        db.session.commit()

    if MajorEvents.query.count() == 0:
        new_major_event = MajorEvents(
            name='Youth Conference',
            description='Youth Conference',
            image='https://www.youtube.com/watch?v=8c7B2v1b5wQ',
            date='2020-12-25',
            url='https://www.youtube.com/watch?v=8c7B2v1b5wQ'
        )
        db.session.add(new_major_event)
        db.session.commit()

        new_major_event = MajorEvents(
            name='Youth Conference',
            description='Youth Conference',
            image='https://www.youtube.com/watch?v=8c7B2v1b5wQ',
            date='2020-12-25',
            url='https://www.youtube.com/watch?v=8c7B2v1b5wQ'
        )
        db.session.add(new_major_event)
        db.session.commit()
    
    if Cluster.query.count() == 0:
        new_cluster = Cluster(
            gen_question='How can I overcome fear?',
            answered=False
        )
        db.session.add(new_cluster)
        db.session.commit()

        new_question = Question(
            question='How can I overcome fear?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

        new_question = Question(
            question='How can I overcome fear of failure?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()
        new_cluster = Cluster(
            gen_question='How can I overcome peer pressure?',
            answered=False
        )
        db.session.add(new_cluster)
        db.session.commit()

        new_question = Question(
            question='How can I overcome peer pressure?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

        new_question = Question(
            question='How can i make decisions not based on peer pressure?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

        new_cluster = Cluster(
            gen_question='What is the purpose of my life?',
            answered=False
        )
        db.session.add(new_cluster)
        db.session.commit()

        new_question = Question(
            question='What is the purpose of my life?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

        new_question = Question(
            question='How can I find my purpose in life?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

        new_cluster = Cluster(
            gen_question='How can I strengthen my relationship with God?',
            answered=False
        )
        db.session.add(new_cluster)
        db.session.commit()

        new_question = Question(
            question='How can I strengthen my relationship with God?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

        new_question = Question(
            question='How can I know God more?',
            cluster=new_cluster
        )
        db.session.add(new_question)
        db.session.commit()

    

