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

    def to_dict(self):
        return {
            'id': self.id,
            'gen_question': self.gen_question,
            'questions': [question.to_dict() for question in self.questions],
            'answer_id': self.answer_id
        }


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(200))
    cluster = db.relationship('Cluster', backref='answer')

    def to_dict(self):
        return {
            'id': self.id,
            'answer': self.answer,
            'cluster': [cluster.to_dict() for cluster in self.cluster]
        }

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question', 'cluster_id')

class AnswerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'answer', 'cluster_id')

class ClusterSchema(ma.Schema):
    questions = ma.Nested(QuestionSchema, many=True)
    answer = ma.Nested(AnswerSchema)
    
    class Meta:
        fields = ('id', 'gen_question', 'questions', 'answer_id')