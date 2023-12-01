import traceback
import json
import uuid
import wave
from os import path

import pyaudio
from flask import Flask, request, jsonify, Response
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
from AudioStream import AudioStream


from flask_pymongo import PyMongo


# Example usage:

# # Inserting a workout session
# workout_session = WorkoutSession("2023-11-30T10:00:00", "Gym XYZ")
# mongo.db.workout_sessions.insert_one(workout_session.__dict__)
#
# # Inserting a participant
# participant = Participant("John Doe", 30, "Male", 1)  # Assuming session ID is 1
# mongo.db.participants.insert_one(participant.__dict__)
#
# # Inserting a heart rate measurement
# heart_rate_measurement = HeartRateMeasurement("2023-11-30T10:15:00", 80, 1)  # Assuming participant ID is 1
# mongo.db.heart_rate_measurements.insert_one(heart_rate_measurement.__dict__)
#
# # Inserting an exercise log
# exercise_log = ExerciseLog("Bench Press", 10, 100, "2023-11-30T10:30:00", "2023-11-30T10:35:00", 1)  # Assuming participant ID is 1
# mongo.db.exercise_logs.insert_one(exercise_log.__dict__)
from model.WorkoutDataModel import WorkoutSession

app = Flask(__name__)

# Replace the connection string with your MongoDB URI
uri = "mongodb+srv://user:cse218@groupfit.l7ynwiw.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.get_database("groupfit")
collection = db.get_collection("workout_sessions")



@app.route('/post/workout-data', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        try:
            # Get the JSON data sent by the client
            data = request.get_json()

            # Check if the file exists
            file_name = "data/" + data["datatype"] + '.json'
            file_exists = path.exists(file_name)

            # Append or create the file and write the received data
            with open(file_name, 'a') as file:
                if file_exists:
                    file.write('\n')  # Add a new line before appending
                file.write(str(data))

            return "", 200  # You can adjust the response data and status code as needed
        except Exception:
            print("Error handling the request:")
            traceback.print_exc()
            return 'Error processing request', 400

@app.route('/create-session', methods=["POST"])
def createWorkoutSession():
    if request.method == "POST":

        #get parameters
        request_data = request.get_json()

        new_session = WorkoutSession(request_data["session_name"], request_data["creator_id"])

        #insert session into database
        db.get_collection("workout_sessions").insert_one(new_session.__dict__)

        return "", 200


@app.route('/get-sessions', methods=["GET"])
def getWorkoutSessions():
    if request.method == "GET":

        #get all sessions from database and store in data
        data = db.get_collection("workout_sessions").find({}, {"_id": 0})
        data = list(data)

        return jsonify(data)


@app.route('/join-session', methods=["POST"])
def joinWorkoutSession():
    if request.method == "POST":

        #get parameters
        join_request = request.get_json()

        with open ("data/sessions.json", "r+") as file:

            data = json.load(file)
            session_id = join_request["session_id"]

            # check if session exists in database
            session = db.get_collection("workout_sessions").find_one({"session_id": session_id}, {"_id": 0})
            print(session)

            #if session exists, add participant to session
            if session:
                session["participants"].append(join_request["user_id"])

                #update session in database
                db.get_collection("workout_sessions").update_one({"id": session_id}, {"$set": session})

                return "Joined session.", 200


            return "Session does not exist.", 400



@app.route("/complete-session", methods=["POST"])
def completeWorkoutSession():
    if request.method == "POST":

        #get parameters
        session_id = request.get_json()["session_id"]


        # check if session exists in database
        session = db.get_collection("workout_sessions").find_one({"session_id": session_id})

        #if session exists, add participant to session
        if session:

            #update session in database
            db.get_collection("workout_sessions").update_one({"session_id": session_id}, {"$set": {"active": "false"}})

            return "Session completed.", 200

        else:
            return "Session does not exist.", 400


@app.route('/stream_audio')
def stream_audio():
    audio_stream = AudioStream()

    return Response(audio_stream.generate(), mimetype="audio/mpeg")


# just for testing
@app.route('/data', methods=['GET'])
def get_heart_rate():
    saved_data = read_saved_data()
    if saved_data:
        return jsonify(saved_data), 200
    else:
        return 'No data available', 404


@app.route('/test', methods=['GEt'])
def test():

    print(client)
    print(db)
    print(collection)

    workout_session = WorkoutSession("session 1", "id28982782")
    collection.insert_one(workout_session.__dict__)

    return "hello world", 200

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


