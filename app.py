from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>TRC API</h1><p>This site is a prototype API for TRC.</p>"


if __name__ == "__main__":
    app.run()