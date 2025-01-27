from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os

# creating a Flask app
app = Flask(__name__)

# enabling CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# loading environment variables
load_dotenv()

app.config['API_URL'] = os.getenv('API_URL')
app.config['HEADERS'] = {"Authorization": f"Bearer {os.getenv('HEADERS')}"}

@app.route('/analyze', methods=['OPTIONS', 'POST'])
def analyze_sentiment():
    if request.method == 'OPTIONS':
        return '', 204  # Preflight response
    
    elif request.method == 'POST':
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid request"}), 400

        text = data.get('text')

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        payload = {
            "inputs": text
        }
        response = requests.post(app.config['API_URL'], headers=app.config['HEADERS'], json=payload)
        results = response.json()

        if not results:
            return jsonify({'error': 'No results from the API'}), 500

        print(results[0])

        return jsonify(results[0])