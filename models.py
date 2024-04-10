from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

ma = Marshmallow(app)


class LiveService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean)

class MajorService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    day = db.Column(db.String(200))
    time = db.Column(db.String(200))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(db.String(200))

class Sermons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    date = db.Column(db.String(200))
    url = db.Column(db.String(200))
    type = db.Column(db.String(200))
    #sort by date

class MajorEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    date = db.Column(db.String(200))
    url = db.Column(db.String(200))
    guests = db.relationship('Guest', backref='major_event')

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    major_event_id = db.Column(db.Integer, db.ForeignKey('major_events.id'))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))

class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship('Question', backref='cluster')
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(200))
    clusters = db.relationship('Cluster', backref='answer')
    


class LiveServiceSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date', 'url', 'is_active')

live_service_schema = LiveServiceSchema()
live_services_schema = LiveServiceSchema(many=True)



#create dummy database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
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


if __name__ == '__main__':
    app.run(debug=True) 