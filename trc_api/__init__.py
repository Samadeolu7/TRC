from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from cluster import QuestionMatcher
import os
from flask import Flask
import trc_api.database as models



# Import other models here



def create_app():
    app = models.app
    api = models.api 
    db = models.db 

    CORS(app) 

    jwt = JWTManager(app)

    def create_question_matcher():
        global q_matcher
        q_matcher = QuestionMatcher("model")

    load_dotenv()

    with app.app_context():
        from .models import Cluster  # Import all models here
        db.create_all()  # Create all tables
        create_question_matcher()

    from trc_api.majorevents.bp import major_events_bp
    from trc_api.liveservices.bp import liveservices_bp
    from trc_api.upcomingevents.bp import upcoming_events_bp
    from trc_api.cluster.bp import cluster_bp
    from trc_api.sermons.bp import sermons_bp
    from trc_api.ping.app import ping_bp

    app.register_blueprint(major_events_bp)
    app.register_blueprint(liveservices_bp)
    app.register_blueprint(upcoming_events_bp)
    app.register_blueprint(cluster_bp)
    app.register_blueprint(sermons_bp)
    app.register_blueprint(ping_bp)
    # Register other blueprints here

    return app