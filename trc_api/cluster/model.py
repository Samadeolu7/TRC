from trc_api.database import db, ma

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)
    email = db.Column(db.String(200),nullable=True)
    notified = db.Column(db.Boolean, default=False)


class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gen_question = db.Column(db.String(200),nullable=True)
    questions = db.relationship('Question', backref='cluster')
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'),nullable=True)
    answered = db.Column(db.Boolean, default=False)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(200))
    cluster = db.relationship('Cluster', backref='answer')

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'cluster_id')

class ClusterSchema(ma.Schema):
    questions = ma.Nested(QuestionSchema, many=True)
    
    class Meta:
        fields = ('id', 'gen_question', 'questions', 'answer_id')

