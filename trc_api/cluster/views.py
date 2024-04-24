from flask import jsonify
from flask_restful import Resource, reqparse
from trc_api.cluster.model import Cluster, Question, Answer
# from cluster import QuestionMatcher
from sqlalchemy.exc import SQLAlchemyError
# from trc_api import q_matcher
from trc_api.database import db

class QuestionsList(Resource):
    def __init__(self):
        pass
        # self.matcher = q_matcher

    def get(self):
        clusters = Cluster.query.all()
        return {'clusters': [cluster.to_dict() for cluster in clusters]}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('question', type=str, required=True)
        data = parser.parse_args()

        # Use the QuestionMatcher to find a similar question
        cluster = None #self.matcher.find_similar_accuracy(data['question'])
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

class AnswersList(Resource):
    def get(self):
        answers = Answer.query.all()
        return jsonify([answer.to_dict() for answer in answers])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cluster_id', type=int, required=True)
        parser.add_argument('question', type=str, required=True)
        parser.add_argument('answer', type=str, required=True)
        data = parser.parse_args()

        new_answer = Answer(cluster_id=data['cluster_id'], question=data['question'], answer=data['answer'])
        db.session.add(new_answer)
        try:
            db.session.commit()
            return new_answer.to_dict(), 201
        except SQLAlchemyError:
            db.session.rollback()
            return {"message": "Error occurred"}, 500