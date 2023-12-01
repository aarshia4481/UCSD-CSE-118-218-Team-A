import traceback
import json
import uuid

from flask import Flask, request, jsonify




app = Flask(__name__)



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


        #get parameters
        new_session = request.get_json()


        # make a new UUID for the new session
        new_session["id"] = str(uuid.uuid4())

        #read session file and write a new session
        with open ("data/sessions", "r+") as file:

            print(new_session)

            data = json.load(file)

            #append new session to saved session file
            data["sessions"].append(new_session)#

            file.seek(0)

            json.dump(data, file, indent=4)



            file.close()

            return "", 200


@app.route('/get-sessions', methods=["GET"])
def getWorkoutSessions():
    if request.method == "GET":

        with open ("data/sessions", "r") as file:

            data = json.load(file)

            file.close()

            return jsonify(data), 200


@app.route('/join-session', methods=["POST"])
def joinWorkoutSession():
    if request.method == "POST":

        #get parameters
        join_request = request.get_json()

        with open ("data/sessions", "r+") as file:

            data = json.load(file)

            #find session with id
            for session in data["sessions"]:
                if session["id"] == join_request["session_id"]:

                    #append new user to session
                    session["participants"].append(join_request["user_id"])

                    file.seek(0)

                    json.dump(data, file, indent=4)

                    file.close()

                    return "", 200

            file.close()

            return "Session does not exist.", 400


















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


