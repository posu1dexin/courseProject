from flask import Flask, jsonify, render_template
import requests
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)

# API details
api_key = 'hjnbqBE30xZL11hbT0nOVnDt0aQluOQ0'  # Replace with your actual API key
section = 'home'
api_url = f'https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={api_key}'

# MQTT broker details
broker = 'broker.hivemq.com'
port = 1883
topic = 'nytimes/topstories'

# Route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch and return the data
@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    # Fetch data from the API
    response = requests.get(api_url)
    data = response.json()

    # Save the data to a JSON file
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Convert data to JSON string
    json_data = json.dumps(data)

    # MQTT client setup and publish
    client = mqtt.Client()
    client.connect(broker, port)
    client.publish(topic, json_data)
    print(json_data)
    client.disconnect()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
