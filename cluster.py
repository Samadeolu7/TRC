import os
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity
from annoy import AnnoyIndex
from trc_api.cluster.model import db, Question, Cluster

class QuestionMatcher:
    def __init__(self, model_path):
        self.model = tf.saved_model.load(model_path)
        self.index = None
        self.build_index()

    def embed(self, sentences):
        return self.model(sentences)

    def build_index(self):
        clusters = Cluster.query.all()
        gen_questions = [cluster.gen_question for cluster in clusters]
        if gen_questions:  # Check if gen_questions is not empty
            embeddings = self.embed(gen_questions)
            self.index = AnnoyIndex(embeddings.shape[1], 'angular')
            for i, embedding in enumerate(embeddings):
                self.index.add_item(i, embedding)

    def find_similar(self, question, threshold=0.5):
        question_embedding = self.embed([question])[0]
        most_similar_index, similarity = self.index.get_nns_by_vector(question_embedding, 1, include_distances=True)
        if similarity[0] < threshold:
            return "No similar question found."
        else:
            return Cluster.query.all()[most_similar_index[0]]
        
    def find_similar_accuracy(self, question, threshold=0.7):
        question_embedding = self.embed([question])[0]
        most_similar_indices = self.index.get_nns_by_vector(question_embedding, 10)  # Get the 10 approximate nearest neighbors
        clusters = Cluster.query.all()
        gen_questions = [clusters[i].gen_question for i in most_similar_indices]
        similarities = cosine_similarity([question_embedding], self.embed(gen_questions))
        most_similar_index = np.argmax(similarities)
        if similarities[0, most_similar_index] < threshold:
            return "No similar question found."
        else:
            return clusters[most_similar_indices[most_similar_index]]
# Test the class
# questions = ["What is software engineering?", "What is machine learning?", "What is artificial intelligence?"]
# matcher = QuestionMatcher("model", questions)
# print(matcher.find_similar_accuracy("What is AI?"))