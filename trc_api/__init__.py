from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_cors import CORS
from cluster import QuestionMatcher
import os
from trc_api.database import db, ma
from flask import Flask



# Import other models here



def create_app():
    app = Flask(__name__)
    api = Api(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    CORS(app) 

    jwt = JWTManager(app)
    db.init_app(app)

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

    app.register_blueprint(major_events_bp)
    app.register_blueprint(liveservices_bp)
    app.register_blueprint(upcoming_events_bp)
    app.register_blueprint(cluster_bp)
    # Register other blueprints here

    return app