# In a new file, e.g., major_events.py
from flask import Blueprint
from flask_restful import Api
from .views import QuestionsList, AnswersList

cluster_bp = Blueprint('cluster', __name__)
api = Api(cluster_bp)

api.add_resource(QuestionsList, '/cluster/questions')
api.add_resource(AnswersList, '/cluster/answers')