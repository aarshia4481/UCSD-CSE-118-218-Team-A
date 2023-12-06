import json
import traceback

from bson import ObjectId
from flask import Flask, request, jsonify, Response, stream_with_context
from pymongo.mongo_client import MongoClient

from AudioStream import AudioStream
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
from WorkoutService import WorkoutService
from model.DataModel import WorkoutSession, ExerciseLog

# Example usage:

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



@app.route('/send-workout-data', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        try:
            # Get the JSON data sent by the client
            data = request.get_json()

            if (data["datatype"] == "hr_data"):
                #insert new datapoint into database
                print(db.get_collection("heart_rate_measurements"))
                db.get_collection("heart_rate_measurements").insert_one({"value": data["value"], "user_id": data["user_id"], "workout_session_name": data["workout_session_name"], "timestamp": data["timestamp"]})

            elif data["datatype"] == "rep_counter":

                #insert new datapoint into database
                db.get_collection("exercise_logs").insert_one(ExerciseLog(data["exercise_type"], data["reps_completed"], data["participant_id"], data["workout_session_id"], data["timestamp"]).__dict__)

            return 'Data saved.', 200

        except Exception as e:
            print("Error handling the request:")
            print(e)
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

        session_dict = new_session.__dict__
        for key, value in session_dict.items():
            if isinstance(value, ObjectId):
                session_dict[key] = str(value)  # Convert ObjectId to string


        return json.dumps(session_dict), 200




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

        # check if session exists in database
        session = db.get_collection("workout_sessions").find_one({"session_name": join_request["session_name"]})

        #if session exists, add participant to session
        if session:

                #update session in database
                db.get_collection("workout_sessions").update_one({"session_name": join_request["session_name"]}, {"$push": {"participants": join_request["user_id"]}})

                #retrieve new session data
                updated_session = db.get_collection("workout_sessions").find_one({"session_name": join_request["session_name"]})


                for key, value in updated_session.items():
                    if isinstance(value, ObjectId):
                        updated_session[key] = str(value)  # Convert ObjectId to string

                return json.dumps(updated_session), 200


        else:
                return "Session does not exist.", 400


@app.route("/finish-session", methods=["POST"])
def finsihWorkoutSession():
    if request.method == "POST":

        #get parameters
        session_id = request.get_json()["session_id"]


        # check if session exists in database
        session = db.get_collection("workout_sessions").find_one({"session_id": session_id})

        #if session exists, add participant to session
        if session:

            #update session in database
            db.get_collection("workout_sessions").update_one({"session_id": session_id}, {"$set": {"state": "finished"}})

            return "Session completed.", 200

        else:
            return "Session does not exist.", 400


@app.route("/start-session", methods=["POST"])
def startWorkoutSession():
    if request.method == "POST":

        #get parameters
        session_id = request.get_json()["session_id"]
        session_name = request.get_json()["session_name"]

        workout_service = WorkoutService(session_id, session_name)
        workout_service.start()

        print(session_id)


        return "Session started.", 200


@app.route('/stream_audio/')
def stream_audio():

    if request.method == 'GET':
        session_id = request.args.get('session_id')

    if session_id == None:
        return "No session id provided.", 400


    audio_stream = AudioStream(session_id)

    return Response(audio_stream.generate(), mimetype="audio/mpeg")



## just for testing
@app.route('/test', methods=['GET'])
def test():

    print(client)
    print(db)
    print(collection)


    return "hello world", 200



if __name__ == '__main__':
    app.run(debug=True, port=443, ssl_context=("adhoc"))


