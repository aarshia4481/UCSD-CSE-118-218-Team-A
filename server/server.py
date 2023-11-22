import traceback

from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/data": {"origins": "*"}})
app.config['MONGO_URI'] = 'mongodb://localhost:27017/groupfit'
db = MongoClient(app.config['MONGO_URI'])


@app.route('/post', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        try:

            print(request.data)
            # Get the JSON data sent by the Android client
            data = request.get_json()

            # Process the received data (here, simply printing it)
            print("Received data from Android client:", data)

            # Save the received data to a file
            with open('received_data.json', 'w') as file:
                file.write(str(data))


            # Send a response back to the Android client
            response_data = {'message': 'Received your POST request!'}
            return response_data, 200  # You can adjust the response data and status code as needed
        except Exception:
            print("Error decoding JSON data:")
            traceback.print_exc()
            return 'Error processing request', 400


@app.route('/create-session', methods=["POST"])
def createWorkoutSession():
    if request.method == "POST":
        session_name = request.form['session_name']

        col = db["workout-sessions"]

        dict = {"name": "John", "address": "Highway 37"}

        x = col.insert_one(dict)



# just for testing
@app.route('/data', methods=['GET'])
def get_heart_rate():
    saved_data = read_saved_data()
    if saved_data:
        return jsonify(saved_data), 200
    else:
        return 'No data available', 404


# Function to read the previously saved file
def read_saved_data():
    try:
        with open('received_data.json', 'r') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        return None

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Runs the Flask app on localhost at port 5000
