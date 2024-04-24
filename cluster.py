import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
from trc_api.cluster.model import Cluster

class QuestionMatcher:
    def __init__(self, model_path):
        self.model = tf.saved_model.load(model_path)
        self.embeddings = None
        self.gen_questions = None
        self.clusters = None
        self.build_index()

    def embed(self, sentences):
        return self.model(sentences)

    def build_index(self):
        self.clusters = Cluster.query.all()
        self.gen_questions = [cluster.gen_question for cluster in self.clusters]
        if self.gen_questions:  # Check if gen_questions is not empty
            self.embeddings = self.embed(self.gen_questions)

    def find_similar(self, question, threshold=0.5):
        if self.embeddings is None:
            return "No similar question found."
        question_embedding = self.embed([question])[0]
        similarities = cosine_similarity([question_embedding], self.embeddings)[0]
        most_similar_index = np.argmax(similarities)
        if similarities[most_similar_index] < threshold:
            return "No similar question found."
        else:
            return self.clusters[most_similar_index]

    def find_similar_accuracy(self, question, threshold=0.7):
        if self.embeddings is None:
            return "No similar question found."
        question_embedding = self.embed([question])[0]
        similarities = cosine_similarity([question_embedding], self.embeddings)[0]
        most_similar_index = np.argmax(similarities)
        if similarities[most_similar_index] < threshold:
            return "No similar question found."
        else:
            return self.clusters[most_similar_index]