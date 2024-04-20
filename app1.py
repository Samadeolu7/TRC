from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, marshal_with, fields
from flask_jwt_extended import JWTManager, jwt_required
from dotenv import load_dotenv
import os, json
from jsondb import JsonDB
from flask_cors import CORS
from cluster import QuestionMatcher
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy

from models import Answer, Cluster, ClusterSchema, Question

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
CORS(app) 
db = SQLAlchemy(app)
jwt = JWTManager(app)

load_dotenv()

db = JsonDB('data.json')

q_matcher = QuestionMatcher("model")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'url': fields.String,
    'is_active': fields.Boolean
}


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
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        data = parser.parse_args()

        new_upcoming_service = {
            "id": len(db.read()['UpcomingServices']) + 1,  # Assign new id
            "name": data['name'],
            "description": data['description'],
            "date": data['date'],
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
        parser.add_argument('date', type=str, required=True)
        parser.add_argument('time', type=str, required=True)
        data = parser.parse_args()

        current_data = db.read()
        upcoming_service = next((item for item in current_data['UpcomingServices'] if item['id'] == id), None)
        if upcoming_service:
            upcoming_service['name'] = data['name']
            upcoming_service['description'] = data['description']
            upcoming_service['date'] = data['date']
            upcoming_service['time'] = data['time']
            db.write(current_data)
            return upcoming_service, 200

        return {'message': 'The upcoming service does not exist'}, 404    

# Assuming the models and QuestionMatcher are defined here

class QuestionsList(Resource):
    def __init__(self):
        self.matcher = QuestionMatcher('model')

    def get(self):
        clusters = Cluster.query.all()
        return ClusterSchema.dump(clusters)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question', type=str, required=True)
        data = parser.parse_args()

        # Use the QuestionMatcher to find a similar question
        cluster = self.matcher.find_similar_accuracy(data['question'])
        if isinstance(cluster, Cluster):
            # If a similar question is found, add the question to the cluster and return the answer
            new_question = Question(question=data['question'], cluster_id=cluster.id)
            db.session.add(new_question)
            db.session.commit()
            answer = Answer.query.filter_by(id=cluster.answer_id).first()
            return {'answer': answer.answer}, 200
        else:
            # If no similar question is found, create a new cluster and return a message
            new_cluster = Cluster()
            new_question = Question(question=data['question'], cluster_id=new_cluster.id)
            db.session.add(new_cluster)
            db.session.commit()
            return {'message': 'A new cluster has been created'}, 201

# Assuming the rest of the code is here
    def delete(self, id):
        current_data = db.read()
        question = next((item for item in current_data['questions'] if item['id'] == id), None)
        if question:
            current_data['questions'].remove(question)
            # Remove the question's ID from the corresponding cluster's questions field
            for cluster in current_data['clusters']:
                if question['id'] in cluster['questions']:
                    cluster['questions'].remove(question['id'])
                    break
            db.write(current_data)
            return {'message': 'The question has been deleted'}, 200

        return {'message': 'The question does not exist'}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('question', type=str, required=True)
        parser.add_argument('cluster_id', type=int, required=True)
        data = parser.parse_args()

        current_data = db.read()
        question = next((item for item in current_data['questions'] if item['id'] == id), None)
        if question:
            # If the cluster_id has changed, update the questions fields of the old and new clusters
            if question['cluster_id'] != data['cluster_id']:
                for cluster in current_data['clusters']:
                    if question['id'] in cluster['questions']:
                        cluster['questions'].remove(question['id'])
                    if cluster['id'] == data['cluster_id']:
                        cluster['questions'].append(question['id'])
            question['question'] = data['question']
            question['cluster_id'] = data['cluster_id']
            db.write(current_data)
            return question, 200

        return {'message': 'The question does not exist'}, 404    


class AnswersList(Resource):
    def get(self):
        data = db.read()
        answers = data['answers']
        return jsonify(answers)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cluster_id', type=int, required=True)
        parser.add_argument('question', type=str, required=True)
        parser.add_argument('answer', type=str, required=True)
        data = parser.parse_args()

        new_answer = {
            "id": len(db.read()['answers']) + 1,  # Assign new id
            "cluster_id": data['cluster_id'],
            "question": data['question'],
            "answer": data['answer']
        }

        current_data = db.read()
        current_data['answers'].append(new_answer)
        db.write(current_data)

        return new_answer, 201

    def delete(self, id):
        current_data = db.read()
        answer = next((item for item in current_data['answers'] if item['id'] == id), None)
        if answer:
            current_data['answers'].remove(answer)
            db.write(current_data)
            return {'message': 'The answer has been deleted'}, 200

        return {'message': 'The answer does not exist'}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('cluster_id', type=int, required=True)
        parser.add_argument('question', type=str, required=True)
        parser.add_argument('answer', type=str, required=True)
        data = parser.parse_args()

        current_data = db.read()
        answer = next((item for item in current_data['answers'] if item['id'] == id), None)
        if answer:
            answer['question_id'] = data['question_id']
            answer['answer'] = data['answer']
            db.write(current_data)
            return answer, 200

        return {'message': 'The answer does not exist'}, 404

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
            },
            "/questions": {
                "GET": "Returns a list of all questions",
                "POST": "Creates a new question: Include the cluster_id in the request body for now to assign the question to a cluster",
                "DELETE": "Deletes a question",
                "PUT": "Updates a question"
            },
            "/answers": {
                "GET": "Returns a list of all answers",
                "POST": "Creates a new answer: Include the cluster_id in the request body to assign the answer to a cluster and the generalized question for the cluster",
                "DELETE": "Deletes an answer",
                "PUT": "Updates an answer"
            }
        }
        return guide
api.add_resource(LiveServiceList, '/liveservices', '/liveservices/<int:id>')
api.add_resource(MajorEventsList, '/majorevents', '/majorevents/<int:id>')
api.add_resource(UpcomingServicesList, '/upcomingevents', '/upcomingevents/<int:id>')
api.add_resource(QuestionsList, '/questions', '/questions/<int:id>')
api.add_resource(ApiGuide, '/')


if __name__ == '__main__':
    app.run(debug=True)