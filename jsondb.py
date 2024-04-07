import json
from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


class JsonDB:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        with open(self.file_name, 'r') as f:
            data = json.load(f)
        return data

    def write(self, data):
        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=4)

data = {
    "LiveService": [],
    "MajorService": [],
    "Event": [],
    "Sermons": [],
    "MajorEvents": [],
    "Guest": [],
    "UpcomingServices": []
}

# Create dummy data
data["LiveService"].append({
    "id": 1,
    "name": 'Sunday Service',
    "description": 'Sunday Service',
    "url": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "is_active": True
})

data["LiveService"].append({
    "id": 2,
    "name": 'Wednesday Service',
    "description": 'Wednesday Service',
    "url": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "is_active": True
})

data["LiveService"].append({
    "id": 3,
    "name": 'Friday Service',
    "description": 'Friday Service',
    "url": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "is_active": True
})

data["MajorEvents"].append({
    "id": 1,
    "name": 'Youth Conference',
    "description": 'Youth Conference',
    "image": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "date": '2020-12-25',
    "url": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "guests": []
})

data["MajorEvents"].append({
    "id": 2,
    "name": 'Youth Conference',
    "description": 'Youth Conference',
    "image": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "date": '2020-12-25',
    "url": 'https://www.youtube.com/watch?v=8c7B2v1b5wQ',
    "guests": []
})

# Convert to JSON and write to file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)